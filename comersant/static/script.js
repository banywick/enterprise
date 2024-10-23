document.addEventListener('DOMContentLoaded', function() {
    const table = document.getElementById('data-table');
    const rows = 10;
    const cols = 10;

    // Create table structure
    for (let i = 0; i < rows; i++) {
        const row = document.createElement('tr');
        for (let j = 0; j < cols; j++) {
            const cell = document.createElement('td');
            cell.setAttribute('contenteditable', 'true');
            cell.setAttribute('data-row', i);
            cell.setAttribute('data-col', j);
            cell.addEventListener('blur', saveCellData);
            row.appendChild(cell);
        }
        table.appendChild(row);
    }

    // Load data from server
    fetch('/data')
        .then(response => response.json())
        .then(data => {
            data.forEach(item => {
                const cell = table.rows[item.row].cells[item.col];
                cell.textContent = item.value;
            });
        });

    function saveCellData(event) {
        const cell = event.target;
        const row = cell.getAttribute('data-row');
        const col = cell.getAttribute('data-col');
        const value = cell.textContent;

        fetch('/data/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ row, col, value })
        });
    }
});
