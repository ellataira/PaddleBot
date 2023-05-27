from Reservation import Reservation


class data:
    # CODE = "35780"
    # DAY = ["1", "26"]  # [month, day]
    # TIME = "13:30"
    # COURT_INDEX = "2"
    # NAME0 = "Taira, Kelly"
    # NAME1 = "Krause, Ron"
    # NAME2 = "Hoyt, Mark"

    COURT1 = Reservation("35780", ["4", "7"], "16:30", "2", "Taira, Kelly", "Krause, Ron", "Hoyt, Mark")

    # CODE = "23580"
    # DAY = ["1", "26"]  # [month, day]
    # TIME = "13:30"
    # COURT_INDEX = "2"  ## once a court is filled, it is no longer in the court list <td>s (it has become <th>),
    # NAME0 = "Flodin, TJ"
    # NAME1 = "Lundak, Dan"
    # NAME2 = "Condon, Sean"

    COURT2 = Reservation("23580", ["4", "7"], "16:30",  "2", "Flodin, TJ", "Lundak, Dan", "Condon, Sean")
