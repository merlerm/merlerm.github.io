module Jekyll
  module HideCustomBibtex
    def hideCustomBibtex(input)
      keywords = @context.registers[:site].config['filtered_bibtex_keywords']

      keywords.each do |keyword|
        input = input.gsub(/^.*\b#{keyword}\b *= *\{.*$\n/, '')
      end

      # Clean superscripts in author lists
      input = input.gsub(/(author\s*=\s*\{)([^}]*)(\})/) do
        prefix, authors, suffix = $1, $2, $3
        "#{prefix}#{authors.gsub(/[*†‡§¶‖&^]/, '')}#{suffix}"
      end

      return input
    end
  end
end

Liquid::Template.register_filter(Jekyll::HideCustomBibtex)
