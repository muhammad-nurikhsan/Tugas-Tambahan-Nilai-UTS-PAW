async function loadUsers() {
    const response = await fetch('/api/users');
    const users = await response.json();
    
    const list = document.getElementById('users');
    list.innerHTML = users.map(u => 
        `<li>${u.name} - ${u.email}</li>`
    ).join('');
}

async function createUser() {
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    
    const response = await fetch('/api/users/create', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name, email})
    });
    
    const result = await response.json();
    alert(result.success ? 'User created!' : 'Error!');
    loadUsers();
}

document.addEventListener('DOMContentLoaded', loadUsers);