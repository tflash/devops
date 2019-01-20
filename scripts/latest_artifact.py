import sys
import urllib2
import re
from natsort import natsorted


def menu():
    args = len(sys.argv)
    for i in xrange(args):
        if str(sys.argv[i]) == '-h' or str(sys.argv[i]) == '--help':
            print '\tUsage: python latest_artifact.py [artifactory_url] [?bump]'
            print '\tExample: python latest_artifact.py http://artifactory.mytheverona.com/artifactory/source-downloader-dev/com/ju/source-downloader/ bump'
            quit()

    # piece of sheet here
    try:
        artifactory_url = str(sys.argv[1])
        try:
            bump = str(sys.argv[2])
            hotfix = str(sys.argv[3])
            return artifactory_url, bump, hotfix
        except:
            pass
        try:
            bump = str(sys.argv[2])
            return artifactory_url, bump
        except:
            pass
        try:
            hotfix = str(sys.argv[3])
            return artifactory_url, hotfix
        except:
            pass
        return artifactory_url
    except Exception:
        print 'Unknown: cannot parse argumens'
        sys.exit(3)


def get_index(artifactory_url):
    response = urllib2.urlopen(artifactory_url)
    response = response.read()
    matched = re.findall('<a href="(\d+\.\d+(?:\.\d+)?(?:\.\d+)?\-(?:dev|uat|prod|test))\/?(?:\.zip)?">', response)
    if not matched:
        matched = re.findall('<a href="(\d+\.\d+\.\d+\-\d+)\/">', response)
    print 'Found %s artifacts' % (len(matched)/2)
    return find_last_artif(matched)


def find_last_artif(artifacts):
    sorted_artifs = natsorted(artifacts)
    print 'Sorted as this: %s' % str(sorted_artifs)
    print 'Last artifact is: %s' % str(sorted_artifs[-1])
    # if len(str(artifacts[-1])) == 3:
    #     artifacts[-1] = str(artifacts[-1]) + '0'
    return sorted_artifs[-1]


def gen_new_artif(last_artif):
    number, env = last_artif.split('-')
    dots = re.findall('\.', number)
    if len(dots) == 1:  # means that pattern line 1.16
        number_array = number.split('.')
        start_number = number_array[0] + '.'
        if number_array[1][0] == '0':  # means that pattern line 1.06
            number = int(number_array[1][1:])
            number += 1
            number = str(number).zfill(2)  # add 1 zero to start
        else:
            number = int(number_array[1])
            number += 1
        new_artif = str(start_number) + str(number) + '-' + env
        print 'New artifact will be %s' % new_artif
        print '##teamcity[setParameter name=\'app_version\' value=\'%s\']' % (str(start_number) + str(number))
    elif len(dots) == 2:  # means that pattern 1.1.16
        number_array = number.split('.')
        start_number = number_array[0] + '.' + number_array[1] + '.'
        if number_array[2][0] == '0':  # means that pattern 1.1.06
            number = int(number_array[2][1:])
            number += 1
            number = str(number).zfill(2)  # add 1 zero to start
        else:
            number = int(number_array[2])
            number += 1
        new_artif = str(start_number) + str(number) + '-' + env
        print 'New artifact will be %s' % new_artif
        print '##teamcity[setParameter name=\'app_version\' value=\'%s\']' % (str(start_number) + str(number))


# Only for PHP team
def gen_hotfix_artif(last_artif):
    number, env = last_artif.split('-')
    dots = re.findall('\.', number)
    if len(dots) == 1:
        print 'Sorry, it is not supported for Java apps'
        sys.exit(1)
    elif len(dots) == 2:  # means that pattern 1.1.16 (means it first hotfix)
        start_number = number
        number = '.1'
    elif len(dots) == 3:  # means that pattern 1.1.16.5 (means it already hotfix)
        number_array = number.split('.')
        start_number = number_array[0] + '.' + number_array[1] + '.' + number_array[2] + '.'
        number = int(number_array[3])
        number += 1
    new_artif = str(start_number) + str(number) + '-' + env
    print 'Hotfix artifact will be %s' % new_artif
    print '##teamcity[setParameter name=\'app_version\' value=\'%s\']' % (str(start_number) + str(number))
    return str(start_number) + str(number)


def main():
    answers = []
    menu_answer = menu()
    print menu_answer
    print len(menu_answer)
    if len(menu_answer) == 2 or len(menu_answer) == 3:
        for each in menu_answer:
            answers.append(each)
    else:  # means than only 1 answer (artifactory url)
        answers.insert(0, menu_answer)
    print answers
    if len(answers) == 2:
        if answers[1] == 'bump':
            last = get_index(answers[0])
            print 'Updating artif version'
            gen_new_artif(last)
        elif answers[1] == 'hotfix':
            last = get_index(answers[0])
            print 'Searching verison for hotfix...'
            gen_hotfix_artif(last)
    elif len(answers) == 1:
        last = get_index(menu_answer)
        number, env = last.split('-')
        print 'Leave artif version'
        print '##teamcity[setParameter name=\'app_version\' value=\'%s\']' % number

main()