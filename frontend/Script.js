document.getElementById('registrationForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const dob = document.getElementById('dob').value;
    const phone = document.getElementById('phone').value;

    await fetch('http://localhost:5000/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, email, dob, phone })
    });

    alert('User Registered');
    fetchUsers();
});

async function fetchUsers() {
    const response = await fetch('http://localhost:5000/registrations');
    const users = await response.json();
    
    let usersHTML = '';
    users.forEach(user => {
        usersHTML += `<p>${user.Name} - ${user.Email} - ${user.DateOfBirth}</p>`;
    });

    document.getElementById('usersList').innerHTML = usersHTML;
}

fetchUsers();
