((* if date_and_location_column_template *))
#two-col-entry(
  left-content: [
  #strong[<<entry.position>>], #block([#set text(hyphenate: false)
  ((* if entry.link *)) #box(link("<<entry.link>>")[<<entry.company>>]) ((* else *)) <<entry.company>> ((* endif *)) -- <<entry.location>>
  ])
    ((* if design.entries.short_second_row or date_and_location_column_template.count("\n\n") > main_column_first_row_template.count("\n\n") or design.section_titles.type=="moderncv" *))
    ((* if main_column_second_row_template *))
    #v(-design-text-leading)
    ((* endif *))

    <<main_column_second_row_template|replace("\n\n", "\n\n#v(-design-text-leading)")>>
    ((* endif *))
  ],
  right-content: [
    <<date_and_location_column_template>>
  ],
)
  ((* if not (design.entries.short_second_row or date_and_location_column_template.count("\n\n") > main_column_first_row_template.count("\n\n") or design.section_titles.type=="moderncv") *))
#one-col-entry(
  content: [
    <<main_column_second_row_template|replace("\n\n", "\n\n#v(-design-text-leading)")>>
  ],
)
((* endif *))
((* else *))

#one-col-entry(
  content: [
  #strong[<<entry.position>>], #block([#set text(hyphenate: false)
  ((* if entry.link *)) #box(link("<<entry.link>>")[<<entry.company>>]) ((* else *)) <<entry.company>> ((* endif *)) -- <<entry.location>>
  ])

    ((* if main_column_second_row_template *))
    #v(-design-text-leading)
    ((* endif *))
    <<main_column_second_row_template|replace("\n\n", "\n\n#v(-design-text-leading)")>>
  ],
)
((* endif *))
