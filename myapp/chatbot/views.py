import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from .models import Conversation, ChatMessage
from .ai_engine import get_ai_response


def chatbot_home(request):
    """Renders the main Chatbot interface."""
    conversations = Conversation.objects.all()[:20]
    return render(request, 'chatbot/index.html', {'conversations': conversations})


@csrf_exempt
@require_POST
def api_send_message(request):
    """
    Receives user prompt, queries the AI engine,
    and returns assistant response.
    """
    try:
        data = json.loads(request.body.decode('utf-8'))
        prompt = data.get('prompt', '').strip()
        conv_id = data.get('conversation_id')
        api_key = data.get('api_key', None)

        if not prompt:
            return JsonResponse({'error': 'Message content cannot be empty.'}, status=400)

        # Get or create conversation
        if conv_id:
            try:
                conversation = Conversation.objects.get(id=conv_id)
            except Conversation.DoesNotExist:
                conversation = Conversation.objects.create(title=prompt[:35] + ("..." if len(prompt) > 35 else ""))
        else:
            conversation = Conversation.objects.create(title=prompt[:35] + ("..." if len(prompt) > 35 else ""))

        # Save user message
        user_msg = ChatMessage.objects.create(
            conversation=conversation,
            role='user',
            content=prompt
        )

        # Retrieve prior history for context
        history = list(conversation.messages.all())

        # Generate AI response
        ai_reply = get_ai_response(prompt, conversation_history=history, api_key=api_key)

        # Save assistant message
        assistant_msg = ChatMessage.objects.create(
            conversation=conversation,
            role='assistant',
            content=ai_reply
        )

        conversation.save()  # update updated_at timestamp

        return JsonResponse({
            'success': True,
            'conversation_id': str(conversation.id),
            'conversation_title': conversation.title,
            'reply': ai_reply,
            'timestamp': assistant_msg.timestamp.strftime('%I:%M %p')
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_GET
def api_get_conversations(request):
    """Returns list of conversations for the sidebar."""
    conversations = Conversation.objects.all().values('id', 'title', 'updated_at')
    data = [
        {
            'id': str(c['id']),
            'title': c['title'],
            'time': c['updated_at'].strftime('%b %d, %I:%M %p')
        }
        for c in conversations
    ]
    return JsonResponse({'conversations': data})


@require_GET
def api_get_messages(request, conv_id):
    """Loads all messages for a specific conversation."""
    conversation = get_object_or_404(Conversation, id=conv_id)
    messages = conversation.messages.all()
    data = [
        {
            'id': m.id,
            'role': m.role,
            'content': m.content,
            'timestamp': m.timestamp.strftime('%I:%M %p')
        }
        for m in messages
    ]
    return JsonResponse({
        'conversation_id': str(conversation.id),
        'title': conversation.title,
        'messages': data
    })


@csrf_exempt
@require_POST
def api_delete_conversation(request, conv_id):
    """Deletes a conversation."""
    try:
        conversation = Conversation.objects.get(id=conv_id)
        conversation.delete()
        return JsonResponse({'success': True})
    except Conversation.DoesNotExist:
        return JsonResponse({'error': 'Conversation not found'}, status=404)


@csrf_exempt
@require_POST
def api_clear_all(request):
    """Clears all conversation history."""
    Conversation.objects.all().delete()
    return JsonResponse({'success': True})
