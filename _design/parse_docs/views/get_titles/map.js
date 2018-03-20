function (doc) {
  if(doc.body) {
    doc.body.films.forEach(function(film) {
      emit([doc._id, film.name], 1);
    });
  }
}
