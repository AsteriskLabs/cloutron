from cloutron.view import *
from cloutron.plugin import *
import boto.codedeploy
from time import localtime, strftime
import datetime


class CodeDeployView (TerminalView):

	@classmethod
	def configure_subparser(cls, subparsers):
		sp = subparsers.add_parser('codedeploy', help='display code deploy groups and deployment statuses', aliases=('cd','c'))
		CloutronView.add_generic_arguments(sp)
		sp.set_defaults(func=CodeDeployView)
		
	def apply_cli_config(self):
		super(CodeDeployView, self).apply_cli_config()
		# if self.args.orientation != None:
		#     self.config.orientation = self.args.orientation

	def sigwinch_handler(self, sig, stack):
		self.render()
		
	def render(self):
		self.info = "CodeDeploy Apps [%s]" % self.config.region
		self.title = "[Updated " + strftime("%H:%M:%S", localtime()) + "] Cloutron"
		self.do_render("Loading....")
		while True:
			conn = boto.codedeploy.connect_to_region(self.config.region)
			res = conn.list_applications()
			output = self.colour("", "white", "grey", [])
			for app in res['applications']:
				output = output + "App: %s\n" % app
				dgs = conn.list_deployment_groups(app)
				for dg in dgs['deploymentGroups']:
					output = output + " \_ Deployment Group: %s\n" % dg
					deps = conn.list_deployments(app, dg)
					if len(deps['deployments']) > 0:
						status = ""
						dep = conn.get_deployment(deps['deployments'][0]) 	
						if dep['deploymentInfo']['status'] == "Succeeded":
							status = self.colour("Succeeded", "green", "grey", [])
						elif dep['deploymentInfo']['status'] == "Failed":
							status = self.colour("Failed", "red", "grey", [])
						elif dep['deploymentInfo']['status'] == "InProgress":
							status = self.colour("In Progress", "yellow", "grey", [])
						else:
							status = dep['deploymentInfo']['status']

						completeTime = ""
						if 'completeTime' in dep['deploymentInfo']:
							completeTime = "/" + datetime.datetime.fromtimestamp(dep['deploymentInfo']['completeTime']).strftime("%H:%M:%S")
						output = output + "     Latest Deployment: %s (%s) %s%s\n     Failed: %s In Progress: %s Skipped: %s Succeeded: %s Pending: %s\n" % (deps['deployments'][0], status, datetime.datetime.fromtimestamp(dep['deploymentInfo']['createTime']).strftime('%Y-%m-%d %H:%M:%S'), completeTime, dep['deploymentInfo']['deploymentOverview']['Failed'], dep['deploymentInfo']['deploymentOverview']['InProgress'], dep['deploymentInfo']['deploymentOverview']['Skipped'], dep['deploymentInfo']['deploymentOverview']['Succeeded'], dep['deploymentInfo']['deploymentOverview']['Pending'])

			self.title = "[Updated " + strftime("%H:%M:%S", localtime()) + "] Cloutron"
			self.do_render(output)
			if float(self.config.poll) < 30:
				time.sleep(30)
			else:
				time.sleep(float(self.config.poll))

class CodeDeployViewPlugin(ViewPlugin):
	plugin_type = 'view'
	name = 'codedeploy'
	view_class = CodeDeployView
