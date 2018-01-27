import click
import webbrowser
import re

@click.command()

@click.option("--all-people", "relation", flag_value="", default=True)
@click.option("-f", "--friends", "relation", flag_value="me/friends/")
@click.option("-r", "--friends-of-friends") # r = Second letter of Friends
@click.option("-k", "--friends-of", multiple=True) # k = Known by <user>
@click.option("-!", "--non-friends", is_flag=True, default=False)

@click.option("--any-gender", "gender", flag_value="", default=True)
@click.option("-M", "--male", "gender", flag_value="males/")
@click.option("-F", "--female", "gender", flag_value="females/")

@click.option("--any-interest", "interest", flag_value="", default=True)
@click.option("-m", "--men", "interest", flag_value="males/users-interested/")
@click.option("-w", "--women", "interest", flag_value="females/users-interested/")

@click.option("--any-relationship", "relationship", flag_value="", default=True)
@click.option("-S", "--single", "relationship", flag_value="single/users/")
@click.option("-R", "--relationship", flag_value="in-any-relationship/users/")
@click.option("-O", "--open-relationship", "relationship", flag_value="in-open-relationship/users/")
@click.option("-X", "--married", "relationship", flag_value="married/users/") # X = Crossed, married
@click.option("-C", "--civil-union", "relationship", flag_value="in-civil-union/users/")
@click.option("-P", "--domestic-partnership", "relationship", flag_value="in-domestic-partnership/users/")
@click.option("-E", "--engaged", "relationship", flag_value="engaged/users/")
@click.option("-K", "--complicated", "relationship", flag_value="its-complicated/users/") # K = The sound of C in Complicated
@click.option("-W", "--widowed", "relationship", flag_value="widowed/users/")
@click.option("-T", "--separated", "relationship", flag_value="separated/users/") # T = next available consonant in separaTed
@click.option("-V", "--divorced", "relationship", flag_value="divorced/users/") # D is for Dating, V next available
@click.option("-D", "--dating", "relationship", flag_value="dating/users/")

@click.option("-l", "--location")
@click.option("-l*", "--former-location", multiple=True)
@click.option("-v", "--visited", multiple=True)
@click.option("-h", "--home-resident")
@click.option("-N", "--lives-near")
@click.option("-N*", "--lived-near", multiple=True)

@click.option("-L", "--like", multiple=True)

@click.option("-c", "--company")
@click.option("-c*", "--former-company", multiple=True)
@click.option("-s", "--school") # h = next available consonant in scHool, as -s is reserved for --study
@click.option("-s*", "--former-school", multiple=True)
@click.option("-j", "--job")
@click.option("-t", "--language", multiple=True) # t for Tongue

@click.option("-J", "--major")
@click.option("-J*", "--former-major", multiple=True)

@click.option("-y", "--year")
@click.option("-H", "--month") # H next available
@click.option("-Y", "--year-range")

@click.option("-n", "--name")

@click.option("-I", "--intersection", "operation", flag_value="intersect/", default=True)
@click.option("-U", "--union", "operation", flag_value="union/")
@click.option("-e", "--echo", is_flag=True, default=False)
def search(relation, friends_of_friends, friends_of, non_friends,
           gender,
           interest,
           relationship,
           location, former_location, visited, home_resident, lives_near, lived_near,
           like,
           company, former_company,
           school, former_school,
           job,
           language, major, former_major,
           year, month,
           year_range,
           name,
           operation, echo):
    friends_of_friends = parametrize_friends_of_friends(friends_of_friends)
    friends_of = parametrize_all(friends_of, r"%s/friends/", page=False)
    non_friends = parametrize_flag(non_friends, r"me/non-friends/")
    location = parametrize(location, r"%s/residents/present/")
    former_location = parametrize_all(former_location, r"%s/residents/past/")
    visited = parametrize_all(visited, r"%s/visitors/")
    home_resident = parametrize(home_resident, r"%s/home-residents/")
    lives_near = parametrize(lives_near, r"%s/residents-near/present/")
    lived_near = parametrize_all(lived_near, r"%s/residents-near/past/")
    like = parametrize_all(like, r"%s/likers/")
    company = parametrize(company, r"%s/employees/present/")
    former_company = parametrize_all(former_company, r"%s/employees/past/")
    school = parametrize(school, r"%s/students/present/")
    former_school = parametrize_all(former_school, r"%s/students/past/")
    job = parametrize(job, r"%s/employees/")
    language = parametrize_all(language, r"%s/speakers/")
    major = parametrize(major, r"%s/major/students/present/")
    former_major = parametrize_all(former_major, r"%s/major/students/past/")
    users_born = parametrize_users_born(year, month)
    year_range = parametrize_year_range(year_range)
    name = parametrize(name, r"%s/users-named/", page=False)
    url = f"https://www.facebook.com/search/{relation}{friends_of_friends}{friends_of}{non_friends}{gender}{interest}{relationship}{location}{former_location}{visited}{home_resident}{lives_near}{lived_near}{like}{company}{former_company}{school}{former_school}{job}{language}{major}{former_major}{users_born}{year_range}{name}{operation}"

    if echo:
        print(url)
    else:
        webbrowser.open(url)

def typify(argument, page=True):
    pages_named = "/pages-named" if page else ""
    return f"{argument[1:]}" if argument.startswith("=") else f"str/{argument}{pages_named}"

def parametrize(argument, pattern, page=True):
    return "" if argument is None else pattern % typify(argument, page)

def parametrize_all(arguments, pattern, page=True):
    result = ""
    if arguments is not None:
        for argument in arguments:
            result += parametrize(argument, pattern)
    return result

def parametrize_flag(flag, pattern):
    return pattern if flag else ""

def parametrize_friends_of_friends(depth):
    return "" if depth is None else "me/" + depth * "friend/"

def parametrize_users_born(year, month):
    if year is None:
        return ""
    date = "date"
    result = f"{year}/"
    if month is not None:
        date = "date-2"
        result += f"{month}/"
    return f"{result}/{date}/users-born/"

def parametrize_year_range(year_range):
    return "" if year_range is None else re.sub(r"(\d+)-(\d+)", r"\2/before/users-born/\1/after/users-born/", year_range)

if __name__ == "__main__":
    search()