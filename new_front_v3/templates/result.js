document.getElementById('budgetForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission
    const budgetValue = document.getElementById('budget').value;
    localStorage.setItem('budget', budgetValue); // Store the budget in local storage
    window.location.href = 'input.html'; // Redirect to your first HTML page
});