@REM Convert notebook to HTML and save in html_files folder
jupyter nbconvert --to html "04_Regional_Performance_with_Growth_Trends.ipynb" --output-dir "../docs"


@REM Go to the root of the project to git add everything
cd ..
git add .
git commit -m "Update notebook as .html"
git push origin main
