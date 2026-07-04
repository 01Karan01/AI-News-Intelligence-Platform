import { useParams } from "react-router-dom";

function Event() {

    const { id } = useParams();

    return (

        <h1
        style={{
            textAlign:"center",
            marginTop:"100px"
        }}
        >
            Event {id}
        </h1>

    );
}

export default Event;