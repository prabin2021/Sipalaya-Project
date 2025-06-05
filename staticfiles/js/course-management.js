// Show/hide modals
function showAddModuleModal() {
    const modal = document.getElementById('addModuleModal');
    if (modal) {
        modal.classList.remove('hidden');
    }
}

function showAddLessonModal() {
    const modal = document.getElementById('addLessonModal');
    if (modal) {
        modal.classList.remove('hidden');
    }
}

function hideModals() {
    const moduleModal = document.getElementById('addModuleModal');
    const lessonModal = document.getElementById('addLessonModal');
    if (moduleModal) moduleModal.classList.add('hidden');
    if (lessonModal) lessonModal.classList.add('hidden');
}

// Module functions
async function createModule(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    
    try {
        const response = await fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        });
        
        if (response.ok) {
            window.location.reload();
        } else {
            console.error('Failed to create module');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function editModule(moduleId) {
    // Implementation for editing module
    console.log('Editing module:', moduleId);
}

async function deleteModule(moduleId) {
    if (confirm('Are you sure you want to delete this module?')) {
        try {
            const response = await fetch(`/instructor/modules/${moduleId}/delete/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });
            
            if (response.ok) {
                window.location.reload();
            } else {
                console.error('Failed to delete module');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }
}

// Lesson functions
async function createLesson(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    
    try {
        const response = await fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        });
        
        if (response.ok) {
            window.location.reload();
        } else {
            console.error('Failed to create lesson');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function editLesson(lessonId) {
    // Implementation for editing lesson
    console.log('Editing lesson:', lessonId);
}

async function deleteLesson(lessonId) {
    if (confirm('Are you sure you want to delete this lesson?')) {
        try {
            const response = await fetch(`/instructor/lessons/${lessonId}/delete/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });
            
            if (response.ok) {
                window.location.reload();
            } else {
                console.error('Failed to delete lesson');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }
} 