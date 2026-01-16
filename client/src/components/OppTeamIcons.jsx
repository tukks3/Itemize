import{ apiUrl } from "../components/Api";

function OppTeamIcons({ result, setResult }) {
    const urls = result.opponents.map(opp =>
        opp ? apiUrl(`/api/champ_icons/${opp}.png`) : null
    );

    function handleRemove(i) {
        setResult(prev => {
            return {
                ...prev,
                opponents: prev.opponents.map((opp, idx) =>
                    idx === i ? null : opp
                ),
            }
        })
    }



    return (
        <>
            <div className="os-opp_team_container">
                {urls.map((url, i) => (
                    url ? (
                        <div className="os-opp_icon_container">
                            <img
                                key={url}
                                src={url}
                                loading="lazy"
                                width={48}
                                height={48}
                                alt="opp_icon"
                            />
                            <button
                                className="close_icon"
                                onClick={() => handleRemove(i)}
                                >
                                    &times;
                                </button>
                        </div>
                    ) : (
                        <div key={i} className="os-empty_opp"></div>
                    )
                ))}
            </div>
        </>
        )
}

export default OppTeamIcons;
