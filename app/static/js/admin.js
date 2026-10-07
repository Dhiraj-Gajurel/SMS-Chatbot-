// ADMIN & PORTAL INTERACTIVE HELPER JS
document.addEventListener('DOMContentLoaded', function() {
    // Delete Confirmation
    const deleteButtons = document.querySelectorAll('.btn-confirm-delete');
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this record? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });

    // Auto-dismiss alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 400);
        }, 4000);
    });
});
