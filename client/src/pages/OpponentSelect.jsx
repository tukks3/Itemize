import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom";
import { useSearchParams } from "react-router-dom"

import "./OpponentSelect.css";
import SearchOpp from "../components/SearchOpp";
import AllOppsGrid from "../components/AllOppsGrid";
import OppTeamIcons from "../components/OppTeamIcons";
import SubmitOpps from "../components/SubmitOpps";
import{ apiUrl } from "../components/Api";



function OpponentSelect({ result, setResult }) {
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    const champ = searchParams.get("champ");
    const [error, setError] = useState(null);


    useEffect(() => {
        fetch(apiUrl("/api/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ champName: champ }),
        }))
            .then(r => r.json())
            .then((data) => {
                if (data.error || champ == null) {
                    navigate("/");
                    return;
                }
            })
    }, []);

    return (
        <div className="os-container">
            <h2 className="os-select_title">Select Your Opponents</h2>

            <img className="os-champ_icon" key={champ} src={apiUrl(`/api/champ_icons/${champ}.png`)} loading="lazy" width={48} height={48} alt="champ icon" /> {/* Champ icon */}
            <SearchOpp result={result} setResult={setResult} error={error} setError={setError}/> {/* Search bar */}
            <AllOppsGrid result={result} setResult={setResult} error={error} setError={setError}/> {/* Enemy select table */}
            <OppTeamIcons result={result} setResult={setResult} /> {/* Enemy team portraits */}
            <SubmitOpps result={result}>Find Items</SubmitOpps>
        </div>
    );
}

export default OpponentSelect;
