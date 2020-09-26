<p align="center">
<h3 align="center">RSS2Pocket</h3>

<p align="center">
An awesome tool to save articles from RSS feed to Pocket automatically.
</p>

<p align="center">
<a href="https://github.com/hankliao87/RSS2Pocket/actions?query=workflow%3Arun">
<img src="https://img.shields.io/github/workflow/status/hankliao87/RSS2Pocket/run.svg?style=flat-square&label=run" alt=""></a>
<a href="https://github.com/hankliao87/RSS2Pocket/graphs/contributors">
<img src="https://img.shields.io/github/contributors/hankliao87/RSS2Pocket.svg?style=flat-square" alt=""></a>
<a href="https://github.com/hankliao87/RSS2Pocket/network/members">
<img src="https://img.shields.io/github/forks/hankliao87/RSS2Pocket.svg?style=flat-square" alt=""></a>
<a href="https://github.com/hankliao87/RSS2Pocket/stargazers">
<img src="https://img.shields.io/github/stars/hankliao87/RSS2Pocket.svg?style=flat-square" alt=""></a>
<a href="https://github.com/hankliao87/RSS2Pocket/issues">
<img src="https://img.shields.io/github/issues/hankliao87/RSS2Pocket.svg?style=flat-square" alt=""></a>
<a href="https://github.com/hankliao87/RSS2Pocket/blob/master/LICENSE.txt">
<img src="https://img.shields.io/github/license/hankliao87/RSS2Pocket.svg?style=flat-square" alt=""></a>
</p>

</p>

## About the Project
I used to use IFTTT to [save articles from RSS feed to Pocket](https://ifttt.com/applets/gnf8UbSV).  
But in Sept. 2020, [IFTTT starts the Pro plan which makes the Standard plan can only create 3 applets](https://ifttt.com/plans).  
Therefore, I try to use GitHub Action to do the jobs.

This project will execute the python script every hour,  
and it will save articles which were posted from RSS feed to Pocket.

## Getting Started

### Install Dependencies
1. `$ python3 -m pip install --upgrade pip`
2. `$ pip3 install -r requirements.txt`

### Get Pocket Token
Please follow
[GETTING STARTED WITH THE POCKET DEVELOPER API](https://www.jamesfmackenzie.com/getting-started-with-the-pocket-developer-api/)
to get `consumer_key` and `access_token`.

## Usage

### GitHub Action
1. Fork this project
2. Edit rss.txt
3. Fill `consumer_key` and `access_token` in the Secrets tab in Settings.

### CLI
1. Edit rss.txt
2. `$ CONSUMER_KEY='consumer_key' ACCESS_TOKEN='access_token' python main.py`


## Known Issues

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Project Link: [https://github.com/hankliao87/RSS2Pocket](https://github.com/hankliao87/RSS2Pocket)

## Acknowledgements
- [GETTING STARTED WITH THE POCKET DEVELOPER API](https://www.jamesfmackenzie.com/getting-started-with-the-pocket-developer-api/)
- [Pocket API: Documentation Overview](https://getpocket.com/developer/docs/overview)
- [Best README Template](https://github.com/othneildrew/Best-README-Template)

