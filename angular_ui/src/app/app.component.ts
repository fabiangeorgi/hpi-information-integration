import {Component, OnInit, ViewChild} from '@angular/core';
import {FormControl} from "@angular/forms";
import {map, Observable, startWith} from "rxjs";
import 'anychart'

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'Information Integration Stock Data';
  options = [
    "1&1",
    "AUTO1",
    "Aareal Bank",
    "Adidas",
    "Adler Real Estate",
    "Affimed",
    "Aixtron",
    "Allianz",
    "Atai Life Sciences",
    "Atoss",
    "Aurubis",
    "BASF",
    "BMW",
    "BayWa",
    "Bayer",
    "Bechtle",
    "Beiersdorf",
    "Bilfinger",
    "BioNTech",
    "Biotest",
    "Borussia Dortmund",
    "Brenntag",
    "CEWE",
    "CTS Eventim",
    "Cancom",
    "Carl Zeiss Meditec",
    "Commerzbank",
    "Compleo Charging Solutions",
    "CompuGroup Medical",
    "Continental",
    "Covestro",
    "CropEnergies",
    "Curevac",
    "DMG Mori",
    "DWS Group",
    "Daimler Truck",
    "Delivery Hero",
    "Dermapharm",
    "Deutsche Bank",
    "Deutsche Börse",
    "Deutsche EuroShop",
    "Deutsche Post",
    "Deutsche Telekom",
    "Deutsche Wohnen",
    "Drägerwerk",
    "Dürr",
    "E.ON",
    "Eckert & Ziegler",
    "EnBW Energie",
    "Encavis",
    "Evonik Industries",
    "Evotec",
    "Fielmann",
    "Fraport",
    "Freenet",
    "Fresenius",
    "Fresenius Medical Care",
    "Fuchs Petrolub",
    "GAG Immobilien",
    "GEA Group",
    "Gateway Real Estate",
    "Gelsenwasser",
    "Gerresheimer",
    "Grenke",
    "HELLA",
    "HUGO BOSS",
    "Hamburger Hafen",
    "Hannover Rück",
    "Hapag-Lloyd",
    "HeidelbergCement",
    "HelloFresh",
    "Henkel",
    "Hensoldt",
    "Hochtief",
    "Hornbach Baumarkt",
    "Hornbach Holding",
    "Hypoport",
    "Immatics",
    "Indus Holding",
    "Infineon",
    "InflaRx",
    "Jenoptik",
    "Jumia",
    "Jungheinrich",
    "K+S",
    "KAP",
    "KION Group",
    "KWS",
    "Knorr-Bremse",
    "Krones",
    "Kuka",
    "LEG Immobilien",
    "Lanxess",
    "Lechwerke",
    "Lilium",
    "Lufthansa",
    "MTU Aero Engines",
    "MVV Energie",
    "MYT Netherlands Parent (Mytheresa)",
    "Mainova",
    "Mainz Biomed",
    "Mensch und Maschine",
    "Mercedes-Benz",
    "Merck",
    "Metro",
    "Mister Spex",
    "Morphosys",
    "Munich RE (Münchener Rück)",
    "Mynaric",
    "Nemetschek",
    "New Work",
    "Nordex",
    "Norma Group",
    "Nürnberger Versicherung",
    "PREOS Real Estate",
    "PUMA",
    "Patrizia Immobilien",
    "Pfeiffer Vacuum",
    "Porsche",
    "ProSiebenSat.1 Media",
    "RWE",
    "Rational",
    "Rheinmetall",
    "Rhön-Klinikum",
    "SAP",
    "SIGNA Sports United",
    "SMA Solar Technology",
    "STRATEC",
    "Salzgitter",
    "Sartorius",
    "Schaeffler",
    "Scout24",
    "Siemens",
    "Siemens Energy",
    "Siemens Healthineers",
    "Siltronic",
    "Simona",
    "Sixt",
    "Software",
    "Sono",
    "Ströer",
    "Symrise",
    "Südzucker",
    "TAG Immobilien",
    "TUI",
    "Talanx",
    "TeamViewer",
    "Thyssenkrupp",
    "Traton",
    "Uniper",
    "United Internet",
    "VIB Vermögen",
    "Varta",
    "Verbio",
    "Volkswagen",
    "Vonovia",
    "Wacker Chemie",
    "Wacker Neuson",
    "Wüstenrot & Württembergische",
    "Zalando",
    "Zeal Network",
    "flatexDEGIRO",
    "secunet",
    "trivago"
  ]

  @ViewChild('chartContainer') chartContainer: any;

  filteredOptions: Observable<string[]> | undefined;
  myControl = new FormControl('');
  companySelected: string | null = '';
  stockDataToVisualize = [];
  companyId: number | null = -1;

  ngOnInit() {
    this.filteredOptions = this.myControl.valueChanges.pipe(
      startWith(''),
      map(value => this._filter(value || '')),
    );
  }

  private _filter(value: string): string[] {
    const filterValue = value.toLowerCase();

    return this.options.filter(option => option.toLowerCase().includes(filterValue));
  }


  public async searchCompany(): Promise<void> {
    this.companySelected = this.myControl.getRawValue() as string;
    if (!this.companySelected) {
      return;
    }

    const body = {
      "query": {
        "query_string": {
          "query": `${this.companySelected}`
        }
      },
      "size": 10,
      "from": 0,
      "sort": []
    };

    const url = 'http://localhost:9200/stocks/_search?pretty=true'
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    })
    const result = await response.json();

    if (result['hits']['hits'].length < 1) {
      return;
    }

    this.companyId = result['hits']['hits'][0]['_source']['stock_id'];
    this.stockDataToVisualize = result['hits']['hits'][0]['_source']['stockEntry'];
    this.stockDataToVisualize.sort((date1, date2) => date1 - date2);
    await this.visualizeData();
  }

  public async getHandelsRegisterData(): Promise<any> {
    const body = {
      "query": {
        "match": {
          "reference_company_id": this.companyId
        }
      },
      "size": 100,
      "from": 0,
      "sort": []
    };

    const url = 'http://localhost:9200/corporates/_search?pretty=true'
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    })
    const result = await response.json();

    if (result['hits']['hits'].length < 1) {
      return {};
    }

    const unknownData: { date: string; description: string; }[] = [];
    const prokuraData: { date: string; description: string; }[] = [];
    const vorstandData: { date: string; description: string; }[] = [];
    const hauptversammlungData: { date: string; description: string; }[] = [];
    const insolvenzData: { date: string; description: string; }[] = [];

    result['hits']['hits'].forEach((entry: any) => {
      const data = entry['_source'];
      // console.log(data['match_score'], data['match_score'] <= 90)
      if (data['match_score'] <= 90) {
        return;
      }

      const dateArray = data['event_date'].split('.');
      const newPersons = data['personsAdd'].map((person: { [x: string]: any; }) => {
        return `${person['first_name']} ${person['last_name']}`
      });
      const removedPersons = data['personsDelete'].map((person: { [x: string]: any; }) => {
        return `${person['first_name']} ${person['last_name']}`
      });

      let newString = ''
      newPersons.forEach((person: string) => {
        newString = newString + person + ', ';
      });
      if (newString != '') {
        newString = newString.slice(0, -2)
      }

      let removedString = ''
      removedPersons.forEach((person: string) => {
        removedString = removedString + person + ', ';
      });
      if (removedString != '') {
        removedString = removedString.slice(0, -2)
      }

      const description = AppComponent.mapEvent(data['event_type'], newString, removedString);

      switch (data['event_type']) {
        case 'EVENT_PROKURA':
          prokuraData.push({
            date: `${dateArray[2]}-${dateArray[1]}-${dateArray[0]}`,
            description: description
          });
          break;
        case 'EVENT_VORSTAND':
          vorstandData.push({
            date: `${dateArray[2]}-${dateArray[1]}-${dateArray[0]}`,
            description: description
          });
          break;
        case 'EVENT_HAUPTVERSAMMLUNG':
          hauptversammlungData.push({
            date: `${dateArray[2]}-${dateArray[1]}-${dateArray[0]}`,
            description: description
          });
          break;
        case 'EVENT_INSOLVENZ':
          insolvenzData.push({
            date: `${dateArray[2]}-${dateArray[1]}-${dateArray[0]}`,
            description: description
          });
          break;
        case 'EVENT_UNKNOWN':
        default:
          unknownData.push({
            date: `${dateArray[2]}-${dateArray[1]}-${dateArray[0]}`,
            description: description
          });
          break;
      }
    });


    return [
      {
        format: "H",
        data: hauptversammlungData,
        fill: "#8fc016"
      },
      {
        format: "V",
        data: vorstandData,
        fill: "#cc1a1a"
      },
      {
        format: "I",
        data: insolvenzData,
        fill: "#dc9222"
      },
      {
        format: "P",
        data: prokuraData,
        fill: "#26d5c1"
      },
      {
        format: "U",
        data: unknownData,
        fill: "#c50fe5"
      },
    ]
  }


  private static mapEvent(event: string, newString: string, removedString: string): string {
    const lengthAdd = newString.split(', ').length;
    const lengthRemove = removedString.split(', ').length
    var gonePerson = 'Gone Person'
    var newPerson = 'New Person'
    if (lengthAdd > 1) {
      newPerson = newPerson + 's'
    }
    if (lengthRemove > 1) {
      gonePerson = gonePerson + 's'
    }
    switch (event) {
      case 'EVENT_PROKURA':
        let prokuraString = 'PROKURA'
        if (newString != '') {
          prokuraString = prokuraString + `\n\n${newPerson}:  (${lengthAdd})\n${newString}`
        }
        if (removedString != '') {
          if (prokuraString != '') {
            prokuraString = prokuraString + `\n`
          }
          prokuraString = prokuraString + `\n${gonePerson}: (${lengthRemove})\n${removedString}`
        }
        return prokuraString;
      case 'EVENT_VORSTAND':
        let returnString = 'VORSTAND'
        if (newString != '') {

          returnString = returnString + `\n\n${newPerson}: (${lengthAdd})\n${newString}`
        }
        if (removedString != '') {
          if (returnString != '') {
            returnString = returnString + `\n`
          }
          returnString = returnString + `${gonePerson}: (${lengthRemove})\n${removedString}`
        }
        return returnString;
      case 'EVENT_HAUPTVERSAMMLUNG':
        let hauptversammlungString = 'HAUPTVERSAMLUNG'
        if (newString != '') {
          hauptversammlungString = hauptversammlungString + `\n\n${newPerson}:  (${lengthAdd})\n${newString}`
        }
        if (removedString != '') {
          if (hauptversammlungString != '') {
            hauptversammlungString = hauptversammlungString + `\n`
          }
          hauptversammlungString = hauptversammlungString + `\n${gonePerson}: (${lengthRemove})\n${removedString}`
        }
        return hauptversammlungString;
      case 'EVENT_INSOLVENZ':
        return 'INVOLVENZ';
      case 'EVENT_UNKNOWN':
      default:
        return 'UNKOWN EVENT';
    }
  }

  private async plotHandelsRegisterData(plot: anychart.core.stock.Plot): Promise<void> {
    const data = await this.getHandelsRegisterData();
    console.log(data);
    if (data.length === 0) {
      return;
    }
    console.log(data);
    // add event markers
    // plot.eventMarkers().data(data);
    // create event markers
    plot.eventMarkers({groups: data});
    // get eventMarkers
    var eventMarkers = plot.eventMarkers();

    // set event markers settings
    eventMarkers.position('series').fieldName('high').type('pin');

    // set event markers tooltip settings
    eventMarkers.tooltip().width(250);

    // set hovered fill
    eventMarkers.hovered().fill('#ff6e40');
  }

  private async visualizeData(): Promise<void> {
    // @ts-ignore
    document.getElementById('chartContainer').innerHTML = "";

    const dataTable = anychart.data.table('date');
    dataTable.addData(this.stockDataToVisualize);
    const mapping = dataTable.mapAs({'open': 'open', 'high': 'high', 'low': 'low', 'close': 'close'});

    // create stock chart
    const chart = anychart.stock();

    // create first plot on the chart
    const plot = chart.plot(0);

    // set grid settings
    plot.yGrid(true).xGrid(true).yMinorGrid(true).xMinorGrid(true);

    const series = plot.candlestick(mapping)
      .name(this.companySelected as string);

    series.legendItem().iconType('rising-falling');

    // create scroller series with mapped data
    chart.scroller().candlestick(mapping);

    // set chart selected date/time range
    await this.plotHandelsRegisterData(plot);

    // create range picker
    const rangePicker = anychart.ui.rangePicker();

    // init range picker
    rangePicker.render(chart);

    // create range selector
    const rangeSelector = anychart.ui.rangeSelector();

    // init range selector
    rangeSelector.render(chart);

    // sets the title of the chart
    chart.title(this.companySelected as string);

    // set container id for the chart
    chart.container('chartContainer');


    // initiate chart drawing
    chart.draw();
  }
}
