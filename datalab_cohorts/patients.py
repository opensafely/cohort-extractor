"""
These methods don't *do* anything; they just return their name and arguments.
This provides a friendlier API then having to build some big nested data
structure by hand and means we can make use of autocomplete, docstrings etc to
make it a bit more discoverable.
"""


# Yes this clashes with the builtin, but we don't need the builtin in this
# context
def all():
    return "all", locals()


def random_sample(percent=None, return_expectations=None):
    """
    A random sample of approximately `percent` patients
    """
    return "random_sample", locals()


def sex(return_expectations=None):
    """
    Returns M, F or empty string if unknown or other
    """
    return "sex", locals()


def age_as_of(
    reference_date,
    # Required keyword
    return_expectations=None,
):
    return "age_as_of", locals()


def registered_as_of(
    reference_date,
    # Required keyword
    return_expectations=None,
):
    """
    All patients registed on the given date
    """
    return "registered_as_of", locals()


def registered_with_one_practice_between(
    start_date,
    end_date,
    # Required keyword
    return_expectations=None,
):
    """
    All patients registered with the same practice through the given period
    """
    return "registered_with_one_practice_between", locals()


def with_complete_history_between(
    start_date,
    end_date,
    # Required keyword
    return_expectations=None,
):
    """
    All patients for which we have a full set of records between the given
    dates
    """
    return "with_complete_history_between", locals()


def most_recent_bmi(
    # Set date limits
    on_or_before=None,
    on_or_after=None,
    between=None,
    minimum_age_at_measurement=16,
    # Required keyword
    return_expectations=None,
    # Add an additional column indicating when measurement was taken
    include_measurement_date=False,
    date_format=None,
    # If we're returning a date, how granular should it be?
    include_month=False,
    include_day=False,
):
    """
    Return patients' most recent BMI (in the defined period) either
    computed from weight and height measurements or, where they are not
    availble, from recorded BMI values. Measurements taken when a patient
    was below the minimum age are ignored. The height measurement can be
    taken before (but not after) the defined period as long as the patient
    was over the minimum age at the time.

    The date of the measurement can be obtained using `date_of("<bmi-column-name>")`.
    If the BMI is computed from weight and height then we use the date of the
    weight measurement for this.
    """
    return "most_recent_bmi", locals()


def mean_recorded_value(
    codelist,
    on_most_recent_day_of_measurement=None,
    # Required keyword
    return_expectations=None,
    # Set date limits
    on_or_before=None,
    on_or_after=None,
    between=None,
    # Add additional columns indicating when measurement was taken
    include_measurement_date=False,
    date_format=None,
    # Deprecated options kept for now for backwards compatibility
    include_month=False,
    include_day=False,
):
    assert codelist.system == "ctv3"
    return "mean_recorded_value", locals()


def with_these_medications(
    codelist,
    # Required keyword
    return_expectations=None,
    # Set date limits
    on_or_before=None,
    on_or_after=None,
    between=None,
    # Matching rule
    find_first_match_in_period=None,
    find_last_match_in_period=None,
    # Set return type
    returning="binary_flag",
    include_date_of_match=False,
    date_format=None,
    # Special (and probably temporary) arguments to support queries we need
    # to do right now. This API will need to be thought through properly at
    # some stage.
    ignore_days_where_these_clinical_codes_occur=None,
    episode_defined_as=None,
    # Deprecated options kept for now for backwards compatibility
    return_binary_flag=None,
    return_number_of_matches_in_period=False,
    return_first_date_in_period=False,
    return_last_date_in_period=False,
    include_month=False,
    include_day=False,
):
    """
    Patients who have been prescribed at least one of this list of medications
    in the defined period
    """
    return "with_these_medications", locals()


def with_these_clinical_events(
    codelist,
    # Required keyword
    return_expectations=None,
    # Set date limits
    on_or_before=None,
    on_or_after=None,
    between=None,
    # Matching rule
    find_first_match_in_period=None,
    find_last_match_in_period=None,
    # Set return type
    returning="binary_flag",
    include_date_of_match=False,
    date_format=None,
    # Special (and probably temporary) arguments to support queries we need
    # to do right now. This API will need to be thought through properly at
    # some stage.
    ignore_days_where_these_codes_occur=None,
    episode_defined_as=None,
    # Deprecated options kept for now for backwards compatibility
    return_binary_flag=None,
    return_number_of_matches_in_period=False,
    return_first_date_in_period=False,
    return_last_date_in_period=False,
    include_month=False,
    include_day=False,
):
    """
    Patients who have had at least one of these clinical events in the defined
    period
    """
    return "with_these_clinical_events", locals()


def categorised_as(category_definitions, return_expectations=None, **extra_columns):
    return "categorised_as", locals()


def satisfying(expression, return_expectations=None, **extra_columns):
    category_definitions = {1: expression, 0: "DEFAULT"}
    if return_expectations is None:
        return_expectations = {}
    return_expectations["category"] = {"ratios": {1: 1, 0: 0}}
    # Remove from local namespace
    del expression
    return "categorised_as", locals()


def registered_practice_as_of(
    date, returning=None, return_expectations=None  # Required keyword
):
    return "registered_practice_as_of", locals()


def address_as_of(
    date,
    returning=None,
    round_to_nearest=None,
    return_expectations=None,  # Required keyword
):
    return "address_as_of", locals()


def care_home_status_as_of(
    date, categorised_as=None, return_expectations=None,  # Required keyword
):
    """
    TPP have attempted to match patient addresses to care homes as stored in
    the CQC database. At its most simple this query returns a boolean
    indicating whether the patient's address (as of the supplied time) matched
    with a care home.

    It is also possible return a more complex categorisation based on
    attributes of the care homes in the CQC database, which can be freely
    downloaded here:
    https://www.cqc.org.uk/about-us/transparency/using-cqc-data

    At present the only imported fields are:
        LocationRequiresNursing
        LocationDoesNotRequireNursing

    But we can ask for more fields to be imported if needed.

    The `categorised_as` argument acts in effectively the same way as for the
    `categorised_as` function except that the only columns that can be referred
    to are those belonging to the care home table (i.e. the two nursing fields
    above) and the boolean `IsPotentialCareHome`
    """
    if categorised_as is None:
        categorised_as = {1: "IsPotentialCareHome", 0: "DEFAULT"}
    return "care_home_status_as_of", locals()


def admitted_to_icu(
    on_or_after=None,
    on_or_before=None,
    between=None,
    find_first_match_in_period=None,
    find_last_match_in_period=None,
    returning="binary_flag",
    date_format=None,
    # Required keyword
    return_expectations=None,
    # Deprecated options kept for now for backwards compatibility
    include_month=True,
    include_day=False,
):
    return "admitted_to_icu", locals()


def with_these_codes_on_death_certificate(
    codelist,
    # Set date limits
    on_or_before=None,
    on_or_after=None,
    between=None,
    # Matching rules
    match_only_underlying_cause=False,
    # Set return type
    returning="binary_flag",
    date_format=None,
    # Deprecated options kept for now for backwards compatibility
    include_month=False,
    include_day=False,
    return_expectations=None,
):
    return "with_these_codes_on_death_certificate", locals()


def died_from_any_cause(
    # Set date limits
    on_or_before=None,
    on_or_after=None,
    between=None,
    # Set return type
    returning="binary_flag",
    date_format=None,
    # Deprecated options kept for now for backwards compatibility
    include_month=False,
    include_day=False,
    return_expectations=None,
):
    return "died_from_any_cause", locals()


def with_death_recorded_in_cpns(
    # Set date limits
    on_or_before=None,
    on_or_after=None,
    between=None,
    # Set return type
    returning="binary_flag",
    date_format=None,
    # Deprecated options kept for now for backwards compatibility
    include_month=False,
    include_day=False,
    return_expectations=None,
):
    return "with_death_recorded_in_cpns", locals()


def date_of(
    source,
    date_format=None,
    # Deprecated options kept for now for backwards compatibility
    include_month=False,
    include_day=False,
    return_expectations=None,
):
    returning = "date"
    return "value_from", locals()


def with_tpp_vaccination_record(
    target_disease_matches=None,
    product_name_matches=None,
    # Set date limits
    on_or_before=None,
    on_or_after=None,
    between=None,
    # Set return type
    returning="binary_flag",
    date_format=None,
    # Matching rule
    find_first_match_in_period=None,
    find_last_match_in_period=None,
    return_expectations=None,
):
    return "with_tpp_vaccination_record", locals()


def with_gp_consultations(
    # Set date limits
    on_or_before=None,
    on_or_after=None,
    between=None,
    # Matching rule
    find_first_match_in_period=None,
    find_last_match_in_period=None,
    # Set return type
    returning="binary_flag",
    date_format=None,
    return_expectations=None,
):
    """
    These are GP-patient interactions, either in person or via phone/video
    call. The concept of a "consultation" in EHR systems is generally broader
    and might include things like updating a phone number with the
    receptionist.
    """
    return "with_gp_consultations", locals()


def with_complete_gp_consultation_history_between(
    start_date,
    end_date,
    # Required keyword
    return_expectations=None,
):
    """
    Because the concept of a "consultation" in EHR systems does not map exactly
    to the GP-patient interaction we're interested in (see above) there is some
    processing required on the part of the EHR vendor to produce the
    consultation record we need. This does not happen automatically as part of
    the GP2GP transfer, and therefore this query can be used to find just those
    patients for which the full history is available.
    """
    return (
        "with_complete_gp_consultation_history_between",
        locals(),
    )


def with_test_result_in_sgss(
    pathogen=None,
    test_result="any",
    # Set date limits
    on_or_before=None,
    on_or_after=None,
    between=None,
    # Matching rule
    find_first_match_in_period=None,
    find_last_match_in_period=None,
    # Set return type
    returning="binary_flag",
    date_format=None,
    return_expectations=None,
):
    """
    Finds lab test results recorded in SGSS (Second Generation Surveillance
    System). Only SARS-CoV-2 results are included in our data extract so this
    will throw an error if the specified pathogen is anything other than
    "SARS-CoV-2".

    `test_result` must be one of: "positive", "negative" or "any"

    The date field used is the date the specimen was taken, rather than the
    date of the lab result.

    There's an important caveat here: where a patient has multiple positive
    tests, SGSS groups these into "episodes" (referred to as
    "Organism-Patient-Illness-Episodes"). Each pathogen has a maximum episode
    duration (usually 2 weeks) and unless positive tests are separated by
    longer than this period they are assumed to be the same episode of illness.
    The specimen date recorded is the *earliest* positive specimen within the
    episode.

    For SARS-CoV-2 the episode length has been set to infinity, meaning that
    once a patient has tested positive every positive test will be part of the
    same episode and record the same specimen date.

    This means that using `find_last_match_in_period` is pointless when
    querying for positive results as only one date will ever be recorded and it
    will be the earliest.

    Our natural assumption, though it doesn't seem to be explicity stated in
    the documentation, is that every negative result is treated as unique.

    For more detail on SGSS in general see:
    https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/739854/PHE_Laboratory_Reporting_Guidelines.pdf

    Information about the SARS-CoV-2 episode length was via email from someone
    at the National Infection Service:

        The COVID-19 episode length in SGSS was set to indefinite, so all
        COVID-19 records from a single patient will be classified as one
        episode. This may change, but is set as it is due to limited
        information around re-infection and virus clearance.

    """
    return "with_test_result_in_sgss", locals()