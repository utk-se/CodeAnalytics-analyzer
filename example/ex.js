import defaultExport from "module-name";
import * as name from "module-name";
import { export1 } from "module-name";
import { export1 as alias1 } from "module-name";
import { export1 , export2 } from "module-name";
import { foo , bar } from "module-name/path/to/specific/un-exported/file";
import { export1 , export2 as alias2 , [...] } from "module-name";
import defaultExport, { export1 [ , [...] ] } from "module-name";
import defaultExport, * as name from "module-name";
import "module-name";
var promise = import("module-name");

class Car {
  constructor(brand) {
    this.carname = brand;
  }
}

function showAlert() {
    var msg = 'Your message here';
    var x = 0 + 1;
    // oof
    /* big oof */
    alert (msg);
}
