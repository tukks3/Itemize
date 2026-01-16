import { useNavigate } from "react-router-dom";
import { useSearchParams } from "react-router-dom"

function SubmitOpps({ result }) {
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    const champId = searchParams.get("champ");

    const hasOpponents = result.opponents.some(opp => opp != null);

    function goNext(e) {
        localStorage.setItem("oppTeam", JSON.stringify(result.opponents));
        navigate(`/results?champ=${encodeURIComponent(champId)}`);
    }

    return (
        <>
            <button
                className="os-submit_button"
                id="submitButton"
                type="button"
                onClick={goNext}
                disabled={!hasOpponents}
            >
                Find Items
            </button>
        </>
    );
}

export default SubmitOpps;
