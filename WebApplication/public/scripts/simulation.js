function formatDate(timestamp) {
    const date = new Date(timestamp * 1000);

    return date.toLocaleString('fr-CA', {
        year: 'numeric',
        month: '2-digit',
        day:'2-digit',
        hour:'2-digit',
        minute:'2-digit'
    });
}

function scrollToSection(id) {
    document.getElementById(id).scrollIntoView({
        behavior: 'smooth'
    });
}

async function loadLatestData() {
    try {
        const response = await fetch('/api/latest');
        const data = await response.json();

        if (!data) return;

        document.getElementById('temperature-value').textContent = 
            `${data.temperature ?? '--'} °C`;

        document.getElementById('luminosite-value').textContent =
            `${data.luminosite ?? '--'} (0-100)`;

        document.getElementById('ouverture-auto-value').textContent =
            `${data.ouverture ?? '--'} %`;

        document.getElementById('mode-value').textContent =
            data.mode ?? '--';

        document.getElementById('opening-percentage').textContent =
            `${data.ouverture ?? '--'}%`;
    } catch (error) {
        console.error('Error loading latest data: ', error);
    }
}

async function loadHistory() {
    try {
        const response = await fetch('/api/history');
        const history = await response.json();

        const table = document.getElementById('history-body');
        table.innerHTML = '';

        history.forEach(row => {
            const tr = document.createElement('tr');
            const badgeClass = row.status === 'En marche' ? 'badge-open' : 'badge-closed';

            tr.classList.add('table-row');

            tr.innerHTML = `
                <td class="td">${formatDate(row.date)}</td>

                <td class="td">
                    <span class="badge ${badgeClass}">
                        ${row.status ?? '--'}
                    </span>
                </td>

                <td class="td">${row.mode ?? '--'}</td>

                <td class="td">${row.temperature ?? '--'} °C</td>

                <td class="td">${row.luminosite ?? '--'}</td>

                <td class="td-ouverture">${row.ouverture ?? '--'}%</td>
            `;

            table.appendChild(tr);
        });
    } catch (error) {
        console.error('Error loading history: ', error);
    }
}

function refreshData() {
    loadLatestData();
    loadHistory();
}

// Refresh every 1 second
refreshData();
setInterval(refreshData, 1000);