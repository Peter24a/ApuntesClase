function Header(el)
  if el.level == 1 then
    return {}
  end
  el.level = el.level - 1
  return el
end

local numero_diagrama = 0

function CodeBlock(el)
  for _, clase in ipairs(el.classes) do
    if clase == "mermaid" then
      numero_diagrama = numero_diagrama + 1
      return pandoc.RawBlock(
        "latex",
        string.format("\\input{contenido/diagramas/diagrama-%02d}", numero_diagrama)
      )
    end
  end
  return pandoc.RawBlock("latex", "\\begin{verbatim}\n" .. el.text .. "\n\\end{verbatim}")
end

function Pandoc(doc)
  local salida = {}
  for indice, bloque in ipairs(doc.blocks) do
    local siguiente = doc.blocks[indice + 1]
    local es_titulo_diagrama =
      (bloque.t == "Para" or bloque.t == "Plain") and
      pandoc.utils.stringify(bloque) == "Diagrama de flujo:"
    local es_integrador =
      siguiente and siguiente.t == "RawBlock" and
      string.find(siguiente.text or "", "diagrama%-24")
    if es_titulo_diagrama and es_integrador then
      table.insert(salida, pandoc.RawBlock("latex", "\\clearpage"))
    end
    table.insert(salida, bloque)
  end
  return pandoc.Pandoc(salida, doc.meta)
end
