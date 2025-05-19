document.addEventListener('DOMContentLoaded', function() {
    // Add installment progress bars
    const installmentRows = document.querySelectorAll('.field-installment_number');
    installmentRows.forEach(row => {
        const installmentNumber = parseInt(row.textContent);
        const totalInstallments = parseInt(row.closest('tr').querySelector('.field-total_installments').textContent);
        const progress = (installmentNumber / totalInstallments) * 100;
        
        const progressBar = document.createElement('div');
        progressBar.className = 'installment-progress';
        progressBar.innerHTML = `<div class="installment-progress-bar" style="width: ${progress}%"></div>`;
        row.appendChild(progressBar);
    });

    // Add overdue warnings
    const dueDateRows = document.querySelectorAll('.field-next_installment_due');
    dueDateRows.forEach(row => {
        const dueDate = new Date(row.textContent);
        const now = new Date();
        if (dueDate < now) {
            row.classList.add('overdue');
            const warningBadge = document.createElement('span');
            warningBadge.className = 'warning-badge';
            warningBadge.textContent = 'Overdue';
            row.appendChild(warningBadge);
        }
    });

    // Add status colors
    const statusRows = document.querySelectorAll('.field-status');
    statusRows.forEach(row => {
        const status = row.textContent.trim().toLowerCase();
        row.classList.add(`status-${status}`);
    });

    // Add payment type colors
    const paymentTypeRows = document.querySelectorAll('.field-payment_type');
    paymentTypeRows.forEach(row => {
        const type = row.textContent.trim().toLowerCase();
        row.classList.add(`payment-type-${type}`);
    });

    // Add tooltips for warning sent dates
    const warningSentRows = document.querySelectorAll('.field-last_warning_sent');
    warningSentRows.forEach(row => {
        if (row.textContent.trim()) {
            row.title = 'Last warning email sent on ' + row.textContent;
        }
    });

    // Add quick filters
    const filterContainer = document.querySelector('.changelist-form');
    if (filterContainer) {
        const quickFilters = document.createElement('div');
        quickFilters.className = 'quick-filters';
        quickFilters.innerHTML = `
            <a href="?status__exact=pending" class="button">Pending</a>
            <a href="?status__exact=completed" class="button">Completed</a>
            <a href="?payment_type__exact=installment" class="button">Installments</a>
            <a href="?payment_type__exact=full" class="button">Full Payments</a>
        `;
        filterContainer.insertBefore(quickFilters, filterContainer.firstChild);
    }
}); 