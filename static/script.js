document.querySelector("form").addEventListener("submit", function (event) {
    event.preventDefault(); // Impede o envio do formulário de forma tradicional

    const formData = new FormData(event.target); // Captura os dados do formulário

    // Converte os dados do formulário para o formato adequado
    const payload = new URLSearchParams();
    formData.forEach((value, key) => {
        payload.append(key, value);
    });

    // Envia a requisição POST para o Flask
    fetch("/api", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: payload.toString(),
    })
        .then((response) => response.json()) // Converte a resposta em JSON
        .then((data) => {
            const jobsDiv = document.getElementById("jobs");

            if (data.error) {
                jobsDiv.innerHTML = `<p style="color: red;">Erro: ${data.error}</p>`;
            } else if (data.jobs) {
                if (data.jobs.length > 0) {
                    jobsDiv.innerHTML = `
                        <h2>Resultados da Busca:</h2>
                        <ul>
                            ${data.jobs
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
                    jobsDiv.innerHTML = "<p>Nenhuma vaga encontrada.</p>";
                }
            }
        })
        .catch((error) => {
            document.getElementById(
                "jobs"
            ).innerHTML = `<p style="color: red;">Erro ao buscar as vagas: ${error}</p>`;
        });
});
