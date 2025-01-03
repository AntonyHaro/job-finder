const menuButton = document.getElementById("menu-button");
const asideMenu = document.getElementById("menu");
const mainContent = document.getElementById("main");

const loader = document.getElementById("loader");
const filtersContainer = document.getElementById("filters");
const jobsContainer = document.getElementById("jobs");

function isLoading(loading) {
    loader.style.display = loading ? "inline-block" : "none";
}

function displayMessage(message, isError = false) {
    jobsContainer.innerHTML = `<p style="color: ${
        isError ? "red" : "black"
    };">${message}</p>`;
}

function displayJobs(jobs) {
    if (jobs.length > 0) {
        jobsContainer.innerHTML = `
            <h2>Resultados da Busca:</h2>
            <ul class="jobs-container">
                ${jobs
                    .map(
                        (job) => `
                        <li class="job">
                            <h3 class="job-title">${job.job_title}</h3>
                            <div>
                                <p><strong>Empresa:</strong> ${job.company}</p>
                                <p><strong>Localização:</strong> ${
                                    job.location
                                }</p>
                                <p><strong>Publicada em:</strong> ${
                                    job.posted_time
                                }</p>
                                <p><strong>Modalidade:</strong> ${
                                    job.remote
                                }</p>
                                <p><strong>Salário:</strong> ${
                                    job.salary || "Não especificado"
                                }</p>
                            </div>
                            <a href="${
                                job.job_url
                            }" target="_blank" rel="noopener noreferrer">Ver vaga no Linkedin</a>
                        </li>`
                    )
                    .join("")}
            </ul>`;
    } else {
        displayMessage("Nenhuma vaga encontrada.");
    }
}

function displayFilters(filters) {
    const newKeys = {
        keywords: "Palavras-chave",
        work_type: "Tipo de trabalho",
        company_filter: "Empresa (opcional)",
        experience: "Experiência",
        date_posted: "Data de Publicação",
    };

    filtersContainer.innerHTML = `
            ${filters
                .map(
                    (filter) => `
                    <div class="filter">
                        <strong>${newKeys[filter.key]}:</strong>
                        <p>${filter.value || "Não especificado"}</p>
                    </div>
                   `
                )
                .join("")}`;
}

async function fetchJobs(formData) {
    jobsContainer.innerHTML = "";
    isLoading(true);

    const payload = new URLSearchParams();
    const filters = [];

    formData.forEach((value, key) => {
        payload.append(key, value);
        filters.push({ key: key, value: value });
    });

    displayFilters(filters);

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

        if (data.jobs) {
            displayJobs(data.jobs);
        } else {
            displayMessage(
                `Erro: ${data.error || "Erro ao fazer a requisição"}`,
                true
            );
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

menuButton.addEventListener("click", () => {
    if (asideMenu.classList.contains("active")) {
        asideMenu.classList.remove("active");
        menuButton.classList.remove("active");
        mainContent.classList.remove("active");
        return;
    }

    asideMenu.classList.add("active");
    menuButton.classList.add("active");
    mainContent.classList.add("active");
});
