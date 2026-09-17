/**
 * TaskPulse Interactive Client Scripts
 */

function openCreateModal() {
  const modal = document.getElementById('createModal');
  if (modal) {
    modal.classList.add('active');
    const firstInput = modal.querySelector('input[name="title"]');
    if (firstInput) {
      setTimeout(() => firstInput.focus(), 50);
    }
  }
}

function closeCreateModal() {
  const modal = document.getElementById('createModal');
  if (modal) {
    modal.classList.remove('active');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  // Bind top navbar create button
  const navCreateBtn = document.getElementById('openCreateModalBtn');
  if (navCreateBtn) {
    navCreateBtn.addEventListener('click', openCreateModal);
  }

  // Close modal when clicking outside of modal card
  const modal = document.getElementById('createModal');
  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        closeCreateModal();
      }
    });
  }

  // Close modal on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeCreateModal();
    }
  });

  // Auto-dismiss toast notifications after 4 seconds
  const toasts = document.querySelectorAll('.toast');
  toasts.forEach((toast) => {
    setTimeout(() => {
      toast.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(50px)';
      setTimeout(() => toast.remove(), 500);
    }, 4000);
  });
});
