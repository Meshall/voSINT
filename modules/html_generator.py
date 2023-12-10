import json

def generate_html(data, video_file_name):
    sorted_images = sorted(data, key=lambda image: (image.get('date', 'N/A') == 'N/A', image.get('date', '')))

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
        <style>
            body {{
                padding: 20px;
                background: url(bg.png) no-repeat center center fixed;
                -webkit-background-size: cover;
                -moz-background-size: cover;
                -o-background-size: cover;
                font-family: "Press Start 2P";
            }}

            .header {{
                text-align: center;
                margin-bottom: 30px;
            }}
            .h1, h3 {{  
                font-family: "Press Start 2P";
                color: #e89153;
             }}   
            .h2 {{  
                font-family: "Press Start 2P";
                color: #FF5F1F; 
                font-size: small;  
            }}
            .image-card:hover {{
                border: 3px solid #e89153;
                transform: translateY(-10px);
                opacity: 0.7;
            }}
            .image-card {{
                width: 100%;
                margin-bottom: 20px;
                border: 2px solid #216479; /* Vibrant Yellow */
                padding: 10px;
                text-align: left;
                background-color: rgba(11, 13, 33, 0.6); /* Vibrant Blue with opacity */
                color: #0B0D21;
            }}
            .image-card img {{
                width: 100%;
                height: auto;
                margin-bottom: 10px;
            }}
            .image-card-content {{
            overflow: auto; /* Show scrollbars when content overflows */
            }}
            .image-card {{
		width: 100%;
    		margin-bottom: 20px;
    		border: 2px solid #216479; /* Vibrant Yellow */
    		padding: 10px;
    		text-align: left;
    		background-color: rgba(11, 13, 33, 0.6); /* Vibrant Blue with opacity */
    		color: #0B0D21;
		}}
            .engine-icon {{
                width: 20px;
                height: 20px;
                margin-right: 5px;
            }}
            .title {{
                color: #FF48C4; /* Vibrant Yellow */
            }}
            .source a {{
                color: #01F9C6;
            }}
			.p {{
		  		text-align: left;
			   
            }}

            .container {{
            	max-width: 2500px;
            }}
        </style>
        <link href="https://fonts.googleapis.com/css?family=Press+Start+2P&display=swap" rel="stylesheet">
        <link rel="preconnect" href="https://fonts.googleapis.com">
		<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
		<link href="https://fonts.googleapis.com/css2?family=Monoton&display=swap" rel="stylesheet">
    </head>
    <body>
        <div class="container">
            <div class="header">
                <img src="logo.png" style="width: 200px; height: 200px;" alt="Script Logo">
                <h1 class="title">voSINT</h1>
                <h2 class="h2">Video reverse search results by descending order, from the first appearance to the most recent appearance for {video_file_name}</h2>
            </div>
            <div class="row">
    """

    for image in sorted_images:
        if 'thumbnail' in image:
            image_url = image['thumbnail']
        elif 'favicon' in image:
            image_url = image['favicon']
        else:
            print("Thumbnail not found for image:", image)
            continue

        html += f"""

            <div class="col-md-3 mb-3">
                <div class="image-card">
                    <img src="{image_url}" alt="Image">
                    <div class="image-card-content">
                        <p class="source"><strong>Source:</strong> <a href="{image['source']}" target="_blank">{image['source']}</a></p>
                        <p class="source" style="color: blue;"><strong>Source:</strong> <a href="{image['source']}" target="_blank" style="color: green;">{image['source']}</a></p>
                	<p style="color: #00DFFC;"><strong>Position:</strong> {image['position']}</p>
                	<p style="color: #00DFFC;"><strong>Title:</strong> {image['title']}</p>
                	<p style="color: #00DFFC;"><strong>Link:</strong> <a href="{image['link']}" target="_blank" style="color: brown;">{image['link']}</a></p>
                	<p style="color: #00DFFC;"><strong>Displayed link:</strong> {image['displayed_link']}</p>
                	<p style="color: #00DFFC;"><strong>Date:</strong> {image.get('date', 'N/A')}</p>
                	<p style="color: #00DFFC;"><strong>Snippet:</strong> {image['snippet']}</p>
                	<p style="color: #00DFFC;"><strong>Image resolution:</strong> {image.get('image_resolution', 'N/A')}</p>
                    </div>
                </div>
            </div>
        """

    html += """ 
            </div>
        </div>
    </body>
    </html>
    """

    return html
