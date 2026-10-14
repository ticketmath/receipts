# Ticket Math · receipts

**Follow the fare.** The data and the code behind every number in the [Ticket Math](https://www.youtube.com/@ticketmath) videos: where every dollar of a price you paid goes, from plane tickets and hotel nights to rental cars, cruises and shipping.

Each video has its own folder:

| Folder | Video |
|---|---|
| [001-airline-ticket](001-airline-ticket/) | How much of a $400 airline ticket does the airline keep? |
| [002-rental-car](002-rental-car/) | How many rental days a month does a rental car need just to cover what it loses? |

Inside each folder:

- `README.md`: the question, the answer, the method, what the number doesn't show, the sources and any corrections.
- `calc.py`: recomputes every number in the video. Python standard library only, no network.
- `data/`: extracts of the public sources used (annual reports filed with the SEC, government statistics, published fees), with the source URL on every row.
- `numbers.json`: the output of `calc.py`.

Only official data and companies' own filings become numbers. When a source doesn't break a cost out, neither do we.

## Corrections

Found an error? Open an issue with the folder, the line and the source. Corrections are listed in the video's README.

## License

- Code (`*.py`): [MIT](LICENSE).
- Data, text and tables: [CC BY 4.0](LICENSE-DATA.md). Reuse them freely; credit "Ticket Math" with a link to this repository. The underlying public records keep their own terms.
