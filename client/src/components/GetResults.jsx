import{ apiUrl } from "../components/Api";

async function GetResults(champId, oppTeam) {

    const res = await fetch(apiUrl("/api/getResults"), {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            champId,
            oppTeam,
        }),
    });
    const data = await res.json();
    return data;
}

export default GetResults;
