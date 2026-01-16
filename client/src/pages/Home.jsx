import { useEffect } from "react";

import "./Home.css"
import Search from "../components/Search";
import AllChampsGrid from "../components/AllChampsGrid";

function Home({ result, setResult }) {
    useEffect(() => {

        setResult(prev => ({
            ...prev,
            champ: null,
            opponents: Array(5).fill(null),
        }));
    }, [setResult]);

    return(
        <div className="home-container">

            <h2 className="select_title">Select Your Champion</h2>
            <Search setResult={setResult} />

            <AllChampsGrid setResult={setResult}/>


        </div>
    );


}

export default Home;

