import { useParams } from "react-router-dom";

import events from "../../data/events";

function Event() {

    const { id } = useParams();

    const event = events.find(
        item => item.id === Number(id)
    );

    if(!event){

        return <h2>Event not found</h2>;

    }

    return(

        <div>

            <h1>

                {event.icon} {event.title}

            </h1>

            <p>

                {event.date}

            </p>

            <hr/>

            <h2>

                📝 AI Summary

            </h2>

            <p>

                {event.summary}

            </p>

            <hr/>

            <h2>

                📈 Impact

            </h2>

            <ul>

                {event.impact?.map(item=>(

                    <li key={item}>

                        {item}

                    </li>

                ))}

            </ul>

            <hr/>

            <h2>

                👤 People

            </h2>

            <ul>

                {event.people?.map(person=>(

                    <li key={person}>

                        {person}

                    </li>

                ))}

            </ul>

            <hr/>

            <h2>

                🏢 Organizations

            </h2>

            <ul>

                {event.organizations?.map(org=>(

                    <li key={org}>

                        {org}

                    </li>

                ))}

            </ul>

            <hr/>

            <h2>

                📍 Locations

            </h2>

            <ul>

                {event.locations?.map(location=>(

                    <li key={location}>

                        {location}

                    </li>

                ))}

            </ul>

        </div>

    );

}

export default Event;