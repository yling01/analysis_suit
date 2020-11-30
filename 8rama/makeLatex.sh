#!/bin/sh
rm rama.pdf
echo "\documentclass{article}
\usepackage{subfigure}
\usepackage{lipsum}
\usepackage{graphicx}
\usepackage[utf8]{inputenc}" >> rama.pdf
printf "\\\begin{document}" >> rama.pdf




printf "
\\\begin{figure}[ht!]
   \\\begin{center}
      \subfigure{\includegraphics[width=\\\textwidth]{s1_cluster1.png}}
      \subfigure{\includegraphics[width=\\\textwidth]{s1_cluster2.png}}
      \subfigure{\includegraphics[width=\\\textwidth]{s1_cluster3.png}}
      \subfigure{\includegraphics[width=\\\textwidth]{s1_cluster4.png}}
      \subfigure{\includegraphics[width=\\\textwidth]{s1_cluster5.png}}
  		\subfigure{\includegraphics[width=\\\textwidth]{s2_cluster1.png}}
  		\subfigure{\includegraphics[width=\\\textwidth]{s2_cluster2.png}}
  		\subfigure{\includegraphics[width=\\\textwidth]{s2_cluster3.png}}
  		\subfigure{\includegraphics[width=\\\textwidth]{s2_cluster4.png}}
  		\subfigure{\includegraphics[width=\\\textwidth]{s2_cluster5.png}}
	\\\end{center}
\\\end{figure}
" >> rama.pdf



echo "\\\end{document}" >> rama.pdf
pdflatex rama.pdf
rm rama.log rama.tex
