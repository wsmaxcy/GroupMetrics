# GroupMetrics

GroupMetrics is a fun little analytics tool for GroupMe chat groups, enabling users to visualize and gain insights into chat activity, user engagement, and more.

![example](https://github.com/wsmaxcy/Group-Me/blob/main/data/ach.png?raw=true)

## Features

- **Message Analysis**: Dive into message counts, average lengths, and time-of-day activity.
- **User Engagement**: Track likes given and received, and identify top contributors.
- **Lexical Insights**: Discover lexical diversity and the most frequently used words.
- **Swear Word Analysis**: Monitor the use of profanity within the chat.
- **Export Data**: Easily export chat data from GroupMe.
- **Custom Visualizations**: View custom bar graphs, network diagrams, and Sankey diagrams to understand the flow of likes.
- **User Achievements**: Highlight user participation with a dynamic achievements board.

## Installation

To get started with GroupMetrics, follow these steps:

```powershell
git clone https://github.com/yourusername/GroupMetrics.git
```

```powershell
cd GroupMetrics
```

# Install the required dependencies
```powershell
pip install -r requirements.txt
```

## Usage
To run GroupMetrics, execute the following command:

```powershell
python groupmetrics.py
```

## Getting Started

To use GroupMetrics, you'll need to export your GroupMe chat data in a `.json` file. Here's how to do it:

1. Visit [GroupMe Export Page](https://web.groupme.com/profile/export).
2. Choose the chat you want to export and select the option for messages only.
3. Once your export is ready, download the `.json` file to your local machine.

### Importing Your Data

With your `.json` file ready, you can now import it into GroupMetrics:

1. Open GroupMetrics.
2. Click the "Load JSON File" button.
3. Select the `.json` file you downloaded from the GroupMe Export Page.

Upon loading the file, GroupMetrics will automatically generate various graphs and metrics based on the chat data provided by the `.json` file.

## Contributing

Contributions to GroupMetrics are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.

## License

Distributed under the MIT License.

## Contact

Will - will@willmaxcy.com

## Acknowledgements

- [GroupMe API](https://dev.groupme.com)
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)