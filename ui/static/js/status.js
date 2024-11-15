document.addEventListener('DOMContentLoaded', function() {
    const statusElement = document.getElementById('current-status');
    const jobsFoundElement = document.getElementById('jobs-found');
    const jobsProcessedElement = document.getElementById('jobs-processed');
    const applicationsSubmittedElement = document.getElementById('applications-submitted');

    const statusColors = {
        'initializing': 'text-blue-600',
        'running': 'text-blue-600',
        'completed': 'text-green-600',
        'error': 'text-red-600',
        'skipped': 'text-yellow-600'
    };

    function updateUI(data) {
        const statusMessage = getStatusMessage(data.status);
        const statusColor = statusColors[data.status] || 'text-blue-600';
        
        statusElement.className = `mt-2 text-lg font-medium ${statusColor}`;
        statusElement.textContent = statusMessage;

        jobsFoundElement.textContent = data.total_jobs || '0';
        jobsProcessedElement.textContent = data.jobs_processed || '0';
        applicationsSubmittedElement.textContent = data.applications_submitted || '0';
    }

    function getStatusMessage(status) {
        const messages = {
            'initializing': 'Starting automation...',
            'running': 'Applying to jobs...',
            'completed': 'All applications completed!',
            'error': 'An error occurred',
            'skipped': 'Skipped - Already applied'
        };
        return messages[status] || status;
    }

    function pollStatus() {
        fetch('/api/status')
            .then(response => response.json())
            .then(data => {
                updateUI(data);
                setTimeout(pollStatus, 1000);
            })
            .catch(error => {
                console.error('Error:', error);
                setTimeout(pollStatus, 2000);
            });
    }

    pollStatus();
});