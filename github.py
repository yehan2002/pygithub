import json
import requests
import os
class urls:
    '''Contains urls in github api'''
    release = 'https://api.github.com/repos/%s/%s/releases'
    issues = 'https://api.github.com/repos/%s/%s/issues'
    issues2 = 'https://api.github.com/issues'
    issues3 = 'https://api.github.com/user/issues'
    issues4 =  'https://api.github.com/repos/%s/%s/issues/%s/events'
    issues5 = 'https://api.github.com/repos/%s/%s/issues/events'
    issue = 'https://api.github.com/repos/%s/%s/issues'
    label = 'https://api.github.com/repos/%s/%s/labels'
    assignees = 'https://api.github.com/repos/%s/%s/'
    gists = 'https://api.github.com/users/%s/gists'
    gists2 =  'https://api.github.com/gists'
    gistcomment = 'https://api.github.com/gists/%s/comments'
    repo = 'https://api.github.com/user/repos'
    repo2 = 'https://api.github.com/users/%s/repos'
    repo3 = 'https://api.github.com/repos/%s/%s'
    repo4 = 'https://api.github.com/user/starred/%s/%s'
    repo5 = 'https://api.github.com/repos/%s/%s/stargazers'
    repo6 = 'https://api.github.com/users/%s/starred'
class skell:
    """Contains basic json requests and headers"""
    newrelease = '''{"tag_name": "%s",
    "target_commitish": "%s",
    "name": "%s",
    "body": "%s",
    "draft": %s,
    "prerelease": %s}'''
    newgist = '''{"description": "%s",
    "public": %s,
    "files": %s
    }'''
    headers = {'Content-Type':'application/json','Accept':'application/json'}
    uploadheaders = {'Accept': 'application/vnd.github.manifold-preview',
            'Content-Type': 'application/octet-stream'}
    newrepo =''' {
    "name": "%s",
    "description": "%s"
    }'''
class github:
    # TODO: Migration Miscellaneous Organizations Projects Pull Requests Reactions
    # Search SCIM Users Enterprise Git Data
    'Basic functions'
    def __init__(self,user=False,password=False,repo=False,owner=False):
        if user and password:
            self.user(user,password)
        if repo:
            self.setRepo(repo)
        if owner:
            self.setOwner(owner)
    def _jsonify(self,string):
        if string == True:
            return 'true'
        elif string == False:
            return 'false'
        elif string == None:
            return 'null'
        return string.replace('\'','"')
    def _set(self,arg):
        return hasattr(self,arg)
    def _basicset(self):
        if not self._set('auth'):
            raise RuntimeError('Username and password not set.')
        elif not self._set('owner'):
            raise RuntimeError('Repository owner not set')
        elif not self._set('repo'):
            raise RuntimeError(' No repository selected.')
    def user(self,user,password,owner=False):
        self.auth=(user, password)
        if not self._set('owner'):
            self.owner = user
        if owner:
            self.owner = user
    def setRepo(self,repo):
        self.repo = repo
    def setOwner(self,owner):
        self.owner = owner
    'Complex functions'
    '''# Releases'''
    def newRelease(self,tag,description,draft=False,prerelease=False,
        comitish='master',dev = False):
        self._basicset()
        data = skell.newrelease%(tag,comitish,tag,description,
        self._jsonify(draft),self._jsonify(prerelease))
        url = urls.release%(self.owner,self.repo)
        auth = self.auth
        headers = skell.headers
        r = requests.post(url,auth=auth,data=data,headers =headers)
        try:
            self.uploadurl = json.loads(r.text)['upload_url'].split('{')[0]
        except KeyError:
            return False
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            return json.loads(r.text)
    def uploadRelease(self,filen,filename=False,url=False):
        self._basicset()
        if url == False:
            if not self._set('uploadurl'):
                raise RuntimeError('Upload url required')
            else:
                url = self.uploadurl
        if filename == False:
            filename = os.path.basename(filen)
        files = {'file': open(filen, 'rb')}
        url = url + '?name='+filename
        headers = skell.uploadheaders
        auth = self.auth
        r = requests.post(url,auth=auth,headers =headers,files=files)
    '''# Issues'''
    # TODO: labels,milestones,timeline for issuess
    def getRepoIssues(self,state=None,dev=False):
        if not state:
            url = urls.issues%(self.owner,self.repo)
        else:
            url = urls.issues%(self.owner,self.repo)+'?state='+state
        r = requests.get(url,headers=skell.headers)
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            return json.loads(r.text)
    def getAllIssues(self,dev=False):
        url = urls.issues2
        r = requests.get(url,headers=skell.headers,auth=self.auth)
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            try:
                return json.loads(r.text)
            except:
                return r.text
    def getUserIssues(self,dev=False):
        url = urls.issues3
        print url
        r = requests.get(url,headers=skell.headers,auth=self.auth)
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            return json.loads(r.text)
    def newIssue(self,owner,repo,title,content,dev=False):
        url = urls.issue%(self.owner,self.repo)
        data = json.dumps({"title":"%s"%(title),"body":"%s"%(content)})
        r = requests.post(url=url,auth=self.auth,headers=skell.headers,data=data)
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            return json.loads(r.text)['url']
    def editIssue(self,idof,title,content,dev=False):
        url = urls.issue%(self.owner,self.repo)+'/'+idof
        data = json.dumps({"title":"%s"%(title),"body":"%s"%(content)})
        r = requests.patch(url=url,auth=self.auth,headers=skell.headers,data=data)
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            return json.loads(r.text)['url']
    '''Issue lock and unlock'''
    def lockIssue(self,idof,dev=False):
        url = urls.issue%(self.owner,self.repo)+'/'+idof + '/lock'
        r = requests.put(url=url,auth=self.auth,headers=skell.headers)
        if dev:
            return (r.status_code, r.reason , r.text)
        else:
            return r.text
    def unlockIssue(self,idof,dev=False):
        url = urls.issue%(self.owner,self.repo)+'/'+idof + '/lock'
        r = requests.delete(url=url,auth=self.auth,headers=skell.headers)
        if dev:
            return (r.status_code, r.reason , r.text)
        else:
            return r.text
    '''assignees'''
    def assignees(self,dev=False):
        url = urls.assignees%(self.owner,self.repo)+'assignees'
        r = requests.get(url=url,auth=self.auth,headers=skell.headers)
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            return [item['login'] for item in json.loads(r.text)]
    def isAssignee(self,name,dev=False):
        url = urls.assignees%(self.owner,self.repo)+'assignees/'+name
        r = requests.get(url=url,auth=self.auth,headers=skell.headers)
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            if r.status_code == 204:
                return True
            elif r.status_code == 404:
                return False
            else:
                return r.text
    def addAssignees(self,idofissue,users,dev=False):
        assert type(users) == list
        url = urls.issue%(self.owner,self.repo)+'/'+idofissue+'/assignees'
        data = json.dumps({"assignees":users})
        r = requests.post(url=url,auth=self.auth,headers=skell.headers,data=data)
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            return json.loads(r.text)
    def removeAssignees(self,idofissue,users,dev=False):
        assert type(users) == list
        url = urls.issue%(self.owner,self.repo)+'/'+idofissue+'/assignees'
        data = json.dumps({"assignees":users})
        r = requests.delete(url=url,auth=self.auth,headers=skell.headers,data=data)
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            return json.loads(r.text)
    '''Issue Events'''
    def eventsIssue(self,issue=None,dev=False):
        if issue == None:
            url = urls.issues5%(self.owner,self.repo)
        else:
            url = urls.issues4%(self.owner,self.repo,issue)
        r = requests.get(url,headers=skell.headers,auth=self.auth)
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            return json.loads(r.text)
    def eventIssue(self,idof,dev=False):
        url = urls.issues5%(self.owner,self.repo,issue)+idof
        r = requests.get(url,headers=skell.headers,auth=self.auth)
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            return json.loads(r.text)
    '''# Gists'''
    def getGists(self,typeof=False,dev=False):
        if not typeof:
            url = urls.gists%(self.owner)
            r = requests.get(url,headers=skell.headers)
        else:
            url = urls.gists2+'/'+typeof
            r = requests.get(url,headers=skell.headers,auth=self.auth)
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            return json.loads(r.text)
    def getGist(self,idof,revision=False,dev=False):
        if not revision:
            url = urls.gists2+'/'+idof
            r = requests.get(url,headers=skell.headers,auth=self.auth)
        else:
            url = urls.gists2+'/'+idof+'/'+revision
            r = requests.get(url,headers=skell.headers,auth=self.auth)
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            return json.loads(r.text)
    def newGist(self,description,files,public=True,dev=False):
        self._basicset()
        filedata = {}
        for item in files:
            item = os.path.abspath(item)
            data = {"content":open(item,'r').read()}
            filedata[os.path.basename(item)] = data
        payload = skell.newgist%(description,self._jsonify(public),
        json.dumps(filedata))
        r = requests.post(url=urls.gists2,headers=skell.headers,data=payload,
        auth=self.auth)
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            return json.loads(r.text)['id']
    def deleteGist(self,idof):
        url = urls.gists2+'/'+idof
        r = requests.delete(url=url,auth=self.auth,headers=skell.headers)
    '''Gists fork'''
    def forkGist(self,idof):
        url = urls.gists2+'/'+idof+'/forks'
        r = requests.post(url=url,auth=self.auth,headers=skell.headers)
    def forksGist(self,idof,dev=False):
        url = urls.gists2+'/'+idof+'/forks'
        r = requests.get(url=url,auth=self.auth,headers=skell.headers)
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            return json.loads(r.text)
    '''Gist stars'''
    def starGist(self,idof,dev=False):
        url = urls.gists2+'/'+idof+'/star'
        r = requests.put(url=url,auth=self.auth,headers=skell.headers)
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            return json.loads(r.text)
    def unstarGist(self,idof,dev=False):
        url = urls.gists2+'/'+idof+'/star'
        r = requests.delete(url=url,auth=self.auth,headers=skell.headers)
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            return json.loads(r.text)
    def starsGist(self,idof,dev=False):
        url = urls.gists2+'/'+idof+'/star'
        r = requests.get(url=url,auth=self.auth,headers=skell.headers)
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            return json.loads(r.text)
    '''Gist commits'''
    def commitsGist(self,idof,dev=False):
        url = urls.gists2+'/'+idof+'/commits'
        r = requests.put(url=url,auth=self.auth,headers=skell.headers)
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            return json.loads(r.text)
    '''Gist comments'''
    def newCommentGist(self,idof,comment,dev=False):
        url = urls.gistcomment%(idof)
        data = json.dumps({"body":"%s"%(comment)})
        r = requests.post(url=url,auth=self.auth,headers=skell.headers,data=data)
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            return json.loads(r.text)['url']
    def commentsGist(self,idof,dev=False):
        url = urls.gistcomment%(idof)
        r = requests.get(url=url,auth=self.auth,headers=skell.headers)
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            return json.loads(r.text)
    def getCommentGist(self,idofgist,idofcomment,dev=False):
        url = urls.gistcomment%(idofgist)+'/'+idofcomment
        r = requests.get(url=url,auth=self.auth,headers=skell.headers)
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            return json.loads(r.text)
    def editCommentGist(self,idofgist,idofcomment,newcomment,dev=False):
        url = urls.gistcomment%(idofgist)+'/'+idofcomment
        data = json.dumps({"body":"%s"%(newcomment)})
        r = requests.patch(url=url,auth=self.auth,headers=skell.headers,
        data=data)
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            return json.loads(r.text)['url']
    def deleteCommentGist(self,idofgist,idofcomment,dev=False):
        url = urls.gistcomment%(idofgist)+'/'+idofcomment
        r = requests.delete(url=url,auth=self.auth,headers=skell.headers)
        try:
            json.loads(r.text)
        except:
            return True
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            return json.loads(r.text)
    '''# Labels'''
    def labels():
    '''# Repositorys'''
    #TODO:Branches,Collaborators,Comments,Community,Commits,Contents,Deploy Keys
    #Deployments,Downloads,Forks,Invitations,Merging.Pages,Releases,Statistics
    #Statuses,Traffic,Webhooks
    def getRepos(self,user='self',typeof='all',dev=False):
        if user == 'self':
            if typeof == 'all':
                url = urls.repo
            else:
                url = urls.repo+'?visibility='+typeof
            r = requests.get(url,headers=skell.headers,auth=self.auth)

        else:
            url = urls.repo2%(user)
            r = requests.get(url,headers=skell.headers,auth=self.auth)
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            return [item['name'] for item in json.loads(r.text)]
    def getRepo(self,dev=False):
        url = urls.repo3 %(self.owner,self.repo)
        r = requests.get(url,headers=skell.headers,auth=self.auth)
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            return (r.text)
    def createRepo(self,name,description,dev = False):
            self._basicset()
            data = skell.newrepo%(name,description)
            url = urls.repo
            auth = self.auth
            headers = skell.headers
            r = requests.post(url,auth=auth,data=data,headers =headers)
            if dev:
                return (r.status_code, r.reason , json.loads(r.text))
            else:
                return json.loads(r.text)
    def editRepo(self,name,description,dev = False):
            self._basicset()
            data = skell.newrepo%(name,description)
            url = urls.repo3%(self.owner,self.repo)
            auth = self.auth
            headers = skell.headers
            r = requests.patch(url,auth=auth,data=data,headers =headers)
            if dev:
                return (r.status_code, r.reason , json.loads(r.text))
            else:
                return json.loads(r.text)
    def languageRepo(self,dev=False):
        url = urls.repo3 %(self.owner,self.repo) + '/languages'
        r = requests.get(url,headers=skell.headers,auth=self.auth)
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            return (r.text)
    def deleteRepo(self,dev=False):
        url = urls.repo3 %(self.owner,self.repo)
        r = requests.delete(url,headers=skell.headers,auth=self.auth)
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            if r.status_code == 204:
                return True
            return (r.text)
    '''Repo stars'''
    def starRepo(self,dev=False):
        url = urls.repo4%(self.owner,self.repo)
        r = requests.put(url=url,auth=self.auth,headers=skell.headers)
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            if r.status_code == 204:
                return True
            elif r.status_code == 404:
                return False
            return r.status_code
    def unstarRepo(self,dev=False):
        url = urls.repo4%(self.owner,self.repo)
        r = requests.delete(url=url,auth=self.auth,headers=skell.headers)
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            if r.status_code == 204:
                return True
            elif r.status_code == 404:
                return False
            return r.status_code
    def isStarRepo(self,dev=False):
        url = urls.repo4%(self.owner,self.repo)
        r = requests.get(url=url,auth=self.auth,headers=skell.headers)
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            if r.status_code == 204:
                return True
            elif r.status_code == 404:
                return False
            return r.status_code
    def starsRepo(self,dev=False):
        url = urls.repo5%(self.owner,self.repo)
        r = requests.get(url=url,auth=self.auth,headers=skell.headers)
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            return [item['login'] for item in json.loads(r.text)]
    def staredRepos(self,user=False,dev=False):
        if user:
            url = urls.repo6%(user)
        else:
            url = urls.repo6%(self.auth[0])
        r = requests.get(url=url,auth=self.auth,headers=skell.headers)
        if dev:
            return (r.status_code, r.reason , json.loads(r.text))
        else:
            return [item['name'] for item in json.loads(r.text)]
    #TODO: watchers
g = github('yehan2002','cb36b850a65c6e24f236e7d4eacb51499fc82be1','pygithubtest2')
print g.eventsIssue()
print g.staredRepos()
