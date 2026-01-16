import{ apiUrl } from "../components/Api";


function ResultOppTeamIcons({ oppTeam }) {
    const urls = oppTeam.map(opp =>
        opp ? apiUrl(`/api/champ_icons/${opp}.png`) : null
    );

    return (
        <>
            <div className="r-opp_team_container">
                {urls.map((url, i) => (
                    url ? (
                        <div key={url} className="r-opp_icon_container">
                            <img
                                src={url}
                                loading="lazy"
                                width={48}
                                height={48}
                                alt="opp_icon"
                            />
                        </div>
                    ) : (
                        <></>
                    )
                ))}
            </div>
        </>
    )
}
export default ResultOppTeamIcons;
