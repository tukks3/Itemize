import { useNavigate } from "react-router-dom";
import { useState } from "react";

function Search({ result, setResult }) {
    const navigate = useNavigate();
    const [error, setError] = useState(null);

    function handleSubmit(e) {
        e.preventDefault();
        const champName = e.target.elements.champName.value;

        fetch("/api/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ champName }),
        })
        .then(res => res.json())
        .then((data) => {
            if (data.error) {
                setError(data.error);
                return; // Skip rest
            }
            setError(null); // Reset error
            setResult(prev => ({
                ...prev,
                champ: data.champId,
            }));
            navigate(`/opponents?champ=${encodeURIComponent(data.champId)}`);
        });
    };

    return (
        <>
            <form className="search_form" onSubmit={handleSubmit}>
                <input className="search_bar" name="champName" type="search" placeholder="Search champion" autocomplete="off" autoFocus/>
            </form>
            {error && <p>{error}</p>}
        </>
    );
}

export default Search;

