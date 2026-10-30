# Ticket Math · receipts

**Follow the fare.** The data and the code behind every number in the [Ticket Math](https://www.youtube.com/@ticketmath) videos: where every dollar of a price you paid goes, from plane tickets and hotel nights to rental cars, cruises and shipping.

Each video has its own folder:

| Folder | Video |
|---|---|
| [001-airline-ticket](001-airline-ticket/) | How much of a $400 airline ticket does the airline keep? |
| [002-rental-car](002-rental-car/) | How many rental days a month does a rental car need just to cover what it loses? |
| [003-hotel-room](003-hotel-room/) | Who makes money on a hotel room: the owner of the building, or the brand on the door? |
| [004-shipping-container](004-shipping-container/) | What does it cost to get goods from China to your door? |
| [005-spirit-airlines](005-spirit-airlines/) | Spirit filled most of its seats and still went under: what did each passenger cost? |
| [006-cruise-onboard](006-cruise-onboard/) | What does a cruise line earn from you after you board? |
| [007-airport-parking](007-airport-parking/) | Who pays a US airport more: your car or the airlines? |
| [008-hormuz-shipping](008-hormuz-shipping/) | When Hormuz closed, how much of the lost oil did the pipelines around it make up for? |

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
