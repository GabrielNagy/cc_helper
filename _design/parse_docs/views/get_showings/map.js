function (doc) {
    if(doc.body) {
        doc.body.films.forEach(function(film) {
            doc.body.events.forEach(function(event) {
                if (film.id == event.filmId) {
                    emit([doc._id, event.eventDateTime.split(" ")[1] || event.eventDateTime.split("T")[1].split(":").slice(0, -1).join(":"), film.name, event.bookingLink, event.attributeIds, film.length, film.releaseYear], event.eventDateTime.split(" ")[1] || event.eventDateTime.split("T")[1].split(":").slice(0, -1).join(":"));
                }
            });
        });
    }
}
