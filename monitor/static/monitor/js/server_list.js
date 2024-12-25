// server_list.js

// server_list.js
window.deleteServer = function(serverId, serverName) {
    const modal = document.getElementById('deleteConfirmModal');
    const serverNameSpan = document.getElementById('serverNameToDelete');
    const confirmBtn = document.getElementById('confirmDeleteBtn');
    
    serverNameSpan.textContent = serverName;
    modal.classList.remove('hidden');
    
    confirmBtn.onclick = (e) => {
        e.preventDefault();
        // URL'yi düzelttik
        fetch(`/dashboard/delete-server/${serverId}/`, {  // URL yolunu güncelledik
            method: 'DELETE',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            // Animate and remove server card
            const serverCard = document.getElementById(`server-${serverId}`);
            if (serverCard) {
                serverCard.style.transition = 'all 0.5s ease-out';
                serverCard.style.transform = 'scale(0.95)';
                serverCard.style.opacity = '0';
                
                setTimeout(() => {
                    serverCard.style.height = '0';
                    serverCard.style.margin = '0';
                    serverCard.style.padding = '0';
                    
                    setTimeout(() => {
                        serverCard.remove();
                    }, 300);
                }, 200);
            }
            
            closeDeleteModal();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to delete server. Please try again.');
        });

        // Return false to prevent any navigation
        return false;
    };
}

window.addServer = function() {
    const serverName = document.getElementById('serverName').value;
    const serverIp = document.getElementById('serverIp').value;
    const serverPort = document.getElementById('serverPort').value;
    const serverUsername = document.getElementById('serverUsername').value;
    const serverPassword = document.getElementById('serverPassword').value;

    fetch('/dashboard/add_server/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({
            name: serverName,
            ip: serverIp,
            port: serverPort,
            username: serverUsername,
            password: serverPassword
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Server added successfully:', data);
        closeAddServerModal();
        location.reload();  // Reload the page to show the new server
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to add server. Please try again.');
    });

    return false;
}

window.closeDeleteModal = function() {
    const modal = document.getElementById('deleteConfirmModal');
    if (!modal) return;

    const modalContent = modal.querySelector('div');
    if (!modalContent) return;
    
    // Animate modal out
    modalContent.style.transform = 'scale(0.95)';
    modalContent.style.opacity = '0';
    
    setTimeout(() => {
        modal.classList.add('hidden');
        // Reset modal styles for next open
        modalContent.style.transform = 'scale(100)';
        modalContent.style.opacity = '1';
    }, 200);
}