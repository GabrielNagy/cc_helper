function (doc) {
  if(doc.body) {
    doc.body.films.forEach(function(film) {
      doc.body.events.forEach(function(event) {
        if (film.id == event.filmId) {
          emit([doc._id, film.name, event.bookingLink], event.eventDateTime.split(" ")[1]);
        }
      });
    });
  }
}
