import { useEffect, useState, useRef } from "react";
import { useSearchParams } from "react-router-dom";

import{ apiUrl } from "../components/Api";


function AllOppsGrid({ result, setResult, error, setError }) {

    const [icons, setIcons] = useState([]);
    const [searchParams] = useSearchParams();
    const champId = searchParams.get("champ");
    const oppTeam = result.opponents;
    const inFlightRef = useRef(false);

    useEffect(() => {
        fetch(apiUrl("/api/listAllChamps"))
            .then(r => r.json())
            .then(data => setIcons(data.icons))
            .catch(console.error);
    }, []);

    useEffect(() => {
        console.log(result);
    }, [result]);

    async function handleClick(url) {
        if (inFlightRef.current) return;
        inFlightRef.current = true;

        const oppId = url.split("/").at(-1).replace(".png", "");

        try {
            const res = await fetch(apiUrl("/api/validTeam", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    champId,
                    oppTeam: result.opponents,
                    oppName: oppId,
                }),
            }));

            const data = await res.json();
            if (!res.ok) throw new Error(data.error || "Request failed");

            setError(null);

            setResult((prev) => {
                const i = prev.opponents.findIndex((x) => x == null);
                if (i === -1) return prev;

                return {
                    ...prev,
                    opponents: prev.opponents.map((opp, idx) =>
                        idx === i ? oppId : opp
                    ),
                };
            });
        } catch (err) {
            setError(err.message);
        } finally {
            inFlightRef.current = false;
        }
    }

    return (
        <>
            <div className="grid-champ_container">
                {icons.map((url) => (
                    <button key={url} className="grid-champ_icon" onClick={() => handleClick(url)}>
                        <img src={url} loading="lazy" width={48} height={48} alt="opp icon" />
                    </button>
                ))}
            </div>
            <div className="team_error_message"> {error && <p>{error}</p>}</div>
        </>

    )

};

export default AllOppsGrid;
