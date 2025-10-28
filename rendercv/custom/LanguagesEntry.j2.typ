/*
  Custom template for languages entries.
  Renders each language as a two-column row: language (bold) on the left, fluency on the right (emphasized).
  Does NOT render `certificate_file` (saved in the data for website use only).
*/

#two-col-entry(
  left-column-width: 4cm,
  left-content: [
    #strong[<<entry.language>>]
  ],
  right-content: [
    #align(right, [#emph[<<entry.fluency or "">>]])
  ],
)
