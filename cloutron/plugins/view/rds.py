from cloutron.view import *
from cloutron.plugin import *
import boto.rds
from time import localtime, strftime


class RdsView (TerminalView):

	@classmethod
	def configure_subparser(cls, subparsers):
		sp = subparsers.add_parser('relationaldatabases', help='display RDS statuses', aliases=('rds','r'))
		CloutronView.add_generic_arguments(sp)
		sp.set_defaults(func=RdsView)
		
	def apply_cli_config(self):
		super(RdsView, self).apply_cli_config()
		# if self.args.orientation != None:
		#     self.config.orientation = self.args.orientation

	def sigwinch_handler(self, sig, stack):
		self.render()
		
	def render(self):
		self.info = "RDS Instances [%s]" % self.config.region
		self.title = "[Updated " + strftime("%H:%M:%S", localtime()) + "] Cloutron"
		self.do_render("Loading....")
		while True:
			conn = boto.rds.connect_to_region(self.config.region)
			res = conn.get_all_dbinstances()	
			output = self.colour("", "white", "grey", [])
			for r in res:
				status = ""
				endpoint = ""
				if r.status == "available":
					status = self.colour(r.status, "green", "grey", [])
					endpoint = "%s:%s" % (r.endpoint[0], r.endpoint[1])
				elif r.status == "deleting":
					status = self.colour(r.status, "red", "grey", [])
				else:
					status = r.status

				output = output + "%s (%s) %s\n" % (r.id, status, endpoint)


			self.title = "[Updated " + strftime("%H:%M:%S", localtime()) + "] Cloutron"
			self.do_render(output)
			if float(self.config.poll) < 30:
				time.sleep(30)
			else:
				time.sleep(float(self.config.poll))

class RdsViewPlugin(ViewPlugin):
	plugin_type = 'view'
	name = 'rds'
	view_class = RdsView
