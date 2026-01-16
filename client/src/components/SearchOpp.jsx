import { useState } from "react";
import { useSearchParams } from "react-router-dom";

import{ apiUrl } from "../components/Api";

function SearchOpp({ result, setResult, error, setError }) {
    const oppTeam = result.opponents;
    const [searchParams] = useSearchParams();
    const champId = searchParams.get("champ");

    function handleSubmit(e) {
        e.preventDefault();
        setError(null)
        const oppName = e.target.elements.oppName.value;

        e.target.reset();

        fetch(apiUrl("/api/validTeam", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                champId,
                oppTeam,
                oppName,
            }),
        }))
            .then(async (res) => {
                const data = await res.json();
                if (!res.ok) throw new Error(data.error || "Request failed");
                return data;
            })
            .then((data) => {
                setError(null);

                setResult((prev) => {
                    const i = prev.opponents.findIndex((x) => x == null);
                    if (i === -1) return prev;

                    return {
                        ...prev,
                        opponents: prev.opponents.map((opp, idx) =>
                            idx === i ? data.oppId : opp
                        ),
                    };
                });
            })
            .catch((err) => setError(err.message));
    }

    return (
        <>
            <form className="os-search_form" onSubmit={handleSubmit} >
                <input className="os-search_bar" name="oppName" type="search" placeholder="Search champion" autocomplete="off" autoFocus />
            </form>
            <div className="team_error_message"> {error && <p>{error}</p>}</div>
        </>
    );
}

export default SearchOpp;
