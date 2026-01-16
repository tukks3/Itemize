import { useEffect, useState } from "react";
import{ useNavigate } from "react-router-dom";


function AllChampsGrid() {
    const navigate = useNavigate();
    const [icons, setIcons] = useState([]);

    useEffect(() => {
        fetch("/api/listAllChamps")
        .then(r => r.json())
        .then(data => setIcons(data.icons))
        .catch(console.error);
    }, []);

    function handleClick(url) {
        const parts = url.split("/");
        let champId = parts.at(-1);
        champId = champId.replace(".png", "");

        navigate(`/opponents?champ=${encodeURIComponent(champId)}`);

    }

    return(
        <div className="grid-champ_container">
            {icons.map((url) =>(
                <button key={url} className="grid-champ_icon" onClick={() => handleClick(url)}>
                    <img  src={url} loading="lazy" width={48} height={48} alt="champ icon"/>
                </button>
            ))}
        </div>
    );
 }

 export default AllChampsGrid;
