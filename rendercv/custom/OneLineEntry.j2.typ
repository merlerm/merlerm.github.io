#one-col-entry(
  content: [
    ((* if entry.link *))
      #box(link("<<entry.link>>")[#strong[<<entry.label>>]])
      : <<entry.details>>
    ((* else *))
      #strong[<<entry.label>>]: <<entry.details>>
    ((* endif *))
  ]
)
