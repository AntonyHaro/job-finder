const loader = document.getElementById("loader");
const jobContainer = document.getElementById("jobs");

function isLoading(loading) {
    loader.style.display = loading ? "inline-block" : "none";
}

function displayMessage(message, isError = false) {
    jobContainer.innerHTML = `<p style="color: ${
        isError ? "red" : "black"
    };">${message}</p>`;
}

function displayJobs(jobs) {
    if (jobs.length > 0) {
        jobContainer.innerHTML = `
            <h2>Resultados da Busca:</h2>
            <ul>
                ${jobs
                    .map(
                        (job) => `
                        <li>
                            <h3>${job.job_title}</h3>
                            <p><strong>Empresa:</strong> ${job.company}</p>
                            <p><strong>Localização:</strong> ${job.location}</p>
                            <p><a href="${job.job_url}" target="_blank" rel="noopener noreferrer">Ver vaga</a></p>
                        </li>`
                    )
                    .join("")}
            </ul>`;
    } else {
        displayMessage("Nenhuma vaga encontrada.");
    }
}

async function fetchJobs(formData) {
    isLoading(true);
    const payload = new URLSearchParams();
    formData.forEach((value, key) => payload.append(key, value));

    try {
        const response = await fetch("/api", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: payload.toString(),
        });

        if (!response.ok) {
            throw new Error(`Erro ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        if (data.error) {
            displayMessage(`Erro: ${data.error}`, true);
        } else if (data.jobs) {
            displayJobs(data.jobs);
        }
    } catch (error) {
        displayMessage(`Erro ao buscar as vagas: ${error.message}`, true);
    } finally {
        isLoading(false);
    }
}

document.querySelector("form").addEventListener("submit", (event) => {
    event.preventDefault();

    const formData = new FormData(event.target);

    fetchJobs(formData);
});
