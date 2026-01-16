import { useSearchParams } from "react-router-dom"
import { useEffect } from "react";
import { useState } from "react";

import "./Results.css";
import GetResults from "../components/GetResults";
import ResultOppTeamIcons from "../components/ResultOppTeamIcons";
import{ apiUrl } from "../components/Api";

function Results() {

    const [searchParams] = useSearchParams();
    const champId = searchParams.get("champ");

    {/* Validate champ */}
    useEffect(() => {
        fetch(apiUrl("/api/search"), {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ champName: champId }),
        })
            .then(r => r.json())
            .then((data) => {
                if (data.error || champId == null) {
                    navigate("/");
                    return;
                }
            })
    }, []);

    const[oppTeam, setOppTeam] = useState(() => {
        try{
            const saved = localStorage.getItem("oppTeam");
            return saved ? JSON.parse(saved) : [];
        } catch {
            return [];
        }
    });

    console.log(oppTeam)


    const [rows, setRows] = useState([]);

    useEffect(() => {
        async function load() {
            const newRows = await GetResults(champId, oppTeam);
            console.log(typeof newRows);
            setRows(newRows);
        };
        load();
    }, []);

    return (
        <div className="r-container">
            <img className="r-champ_image" src={apiUrl(`api/champ_icons/${champId}.png`)}/>

            <ResultOppTeamIcons oppTeam={oppTeam}/>

            <table className="r-result_table">
                <thead>
                    <tr>
                        <th className="r-table_item_title">Item</th>
                        <th className="r-table_priority_title"># Enemy stats countered</th>
                        <th className="r-table_good_against_title"colSpan="5">Good Against</th>
                    </tr>
                </thead><tbody>
                    {rows.map((row, i) => (
                        <tr className="r-table_body_rows" key={row.item_id ?? i}>
                            <td className="r-table_item_img_container"><img className="table_item_img"key={row.item_icon_url} src={apiUrl(row.item_icon_url)} loading="lazy" width={48} height={48}></img></td>
                            <td className="r-prio_row">{row.priority}</td>
                            <td>
                                <div className="r-good_against_row">
                                    {Object.entries(row.counters ?? {}).map(([key]) => (
                                        <img
                                            key={key}
                                            src={apiUrl(`api/champ_icons/${key}.png`)}
                                            alt={key}
                                            loading="lazy"
                                            width={48}
                                            height={48}/>
                                    ))}
                                </div>
                            </td>
                        </tr>
                    ))}

                </tbody>
            </table>
        </div>
    );
}
export default Results;

