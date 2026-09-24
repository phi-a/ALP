$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot

pdflatex -interaction=nonstopmode -halt-on-error main.tex
if ($LASTEXITCODE -ne 0) { throw "Initial pdflatex pass failed with exit code $LASTEXITCODE." }
bibtex main
if ($LASTEXITCODE -ne 0) { throw "BibTeX failed with exit code $LASTEXITCODE." }
pdflatex -interaction=nonstopmode -halt-on-error main.tex
if ($LASTEXITCODE -ne 0) { throw "Second pdflatex pass failed with exit code $LASTEXITCODE." }
pdflatex -interaction=nonstopmode -halt-on-error main.tex
if ($LASTEXITCODE -ne 0) { throw "Final pdflatex pass failed with exit code $LASTEXITCODE." }

Write-Host "Built $PSScriptRoot\main.pdf"
