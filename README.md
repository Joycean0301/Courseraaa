# Coursera Extension


## Clone repo
```
git clone https://github.com/Joycean0301/Courseraaa.git
```

## Upload extension

Google Chrome -> Setting -> Extensions -> Manage Extensions -> Turn on **Developer mode** -> Load unpacked: Upload folder git

![Screenshot from 2023-06-02 03-03-15](https://github.com/Joycean0301/Courseraaa/assets/103662477/da471081-ae73-451f-8365-ee00c3396781)




## Download question

- Step 1: Go to Coursera Quiz -> Click **Download** button 
- Step 2: Put all txt in `..\Courseraaa\input_folder` folder -> Run file `..\Courseraaa\main.py` -> Input file name subject -> result in: `..\Courseraaa\output_folder`.

![Screenshot from 2023-06-02 03-04-22](https://github.com/Joycean0301/Courseraaa/assets/103662477/5e371b37-e33b-4ca4-948f-340460409f2c)




## Automatically filled

- Step 1: After run `main.py` file, the **data.json** data file contain correct answers located in `..\Courseraaa\output_folder\[name]` folder.
- Step 2: Rename new json path name **URL** in file `..\Courseraaa\feature_fill.js` with the path of **data.json** data file.

![Screenshot from 2023-06-03 00-20-06](https://github.com/Joycean0301/Courseraaa/assets/103662477/eaf4c872-264b-4050-8168-c06a91a54116)

- Step 3: Save file and click `Reload` button on Manage Extensions 

  ![Screenshot from 2023-06-03 00-23-13](https://github.com/Joycean0301/Courseraaa/assets/103662477/af760ae3-e6e4-433e-bdc0-ff8561e82ae3)
  
- Step 4: Go to Coursera Quiz: Enjoy :D
