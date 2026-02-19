@REM Convert notebook to HTML and save in html_files folder
jupyter nbconvert --to html "03_Customer Segmentation (RFM Analysis).ipynb" --output-dir "../docs"


@REM Go to the root of the project to git add everything
cd ..
git add .
git commit -m "Update notebook as .html"
git push origin maincls
